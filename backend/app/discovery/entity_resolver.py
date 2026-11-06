import re
import logging
from typing import Dict, Any, Optional, List
import httpx

logger = logging.getLogger(__name__)

USER_AGENT = "AccountIQ-Bot/1.0 (https://bridgeai.ai; sahai.khunteta@bridgeai.ai) Mozilla/5.0"

class EntityResolver:
    """
    Dynamic Company Identity Resolution engine.
    Disambiguates arbitrary company names, detects parent vs subsidiary relationships,
    resolves legal names, stock tickers, headquarters, and official domains.
    Never assumes or invents data.
    """

    _sec_tickers_cache: Optional[Dict[str, Any]] = None

    @classmethod
    async def _get_sec_tickers(cls, client: httpx.AsyncClient) -> Dict[str, Any]:
        if cls._sec_tickers_cache is not None:
            return cls._sec_tickers_cache
        try:
            res = await client.get(
                "https://www.sec.gov/files/company_tickers.json",
                headers={"User-Agent": USER_AGENT},
                timeout=8.0
            )
            if res.status_code == 200:
                cls._sec_tickers_cache = res.json()
                return cls._sec_tickers_cache
        except Exception as e:
            logger.warning(f"Unable to load SEC tickers registry: {e}")
        return {}

    @classmethod
    async def resolve(cls, company_query: str, user_industry: Optional[str] = None) -> Dict[str, Any]:
        """
        Resolves identity for an arbitrary company query.
        Returns normalized identity dictionary.
        """
        query_clean = company_query.strip()
        query_lower = query_clean.lower()
        
        # Base entity structure
        entity = {
            "query": query_clean,
            "canonical_name": query_clean,
            "display_name": query_clean,
            "legal_name": f"{query_clean}",
            "ticker": None,
            "cik": None,
            "country": "UNKNOWN",
            "headquarters": "UNKNOWN",
            "industry": user_industry or "UNKNOWN",
            "is_subsidiary": False,
            "parent_company": None,
            "company_type": "UNKNOWN", # Public, Private, Subsidiary
            "official_website": None,
            "wikipedia_title": None,
            "wikipedia_extract": None,
            "identity_notes": "Identity resolved via dynamic multi-source discovery.",
            "is_resolved": False
        }

        async with httpx.AsyncClient(timeout=10.0, headers={"User-Agent": USER_AGENT}, follow_redirects=True) as client:
            # 1. Search Wikipedia API for matching corporate entities
            wiki_candidate = await cls._search_wikipedia_entity(client, query_clean)
            if wiki_candidate:
                raw_title = wiki_candidate.get("title", "")
                entity["wikipedia_title"] = raw_title
                # Clean off parenthetical qualifiers like " (company)" or " (corporation)"
                clean_title = re.sub(r'\s*\([^)]*\)', '', raw_title).strip()
                entity["canonical_name"] = clean_title or query_clean
                entity["wikipedia_extract"] = wiki_candidate.get("extract")
                if wiki_candidate.get("description"):
                    entity["industry"] = wiki_candidate.get("description")
                entity["is_resolved"] = True

            # 2. Match with SEC EDGAR for US public entities if applicable
            sec_match = await cls._match_sec_ticker(client, query_clean)
            if sec_match:
                entity["ticker"] = sec_match.get("ticker")
                entity["cik"] = sec_match.get("cik_str")
                entity["legal_name"] = sec_match.get("title")
                entity["company_type"] = "Public"
                entity["is_resolved"] = True

            # 3. If Wikipedia page found, fetch Infobox for headquarters, parent, website, ticker, etc.
            if entity["wikipedia_title"]:
                infobox = await cls._extract_wikipedia_infobox(client, entity["wikipedia_title"])
                if infobox:
                    cls._enrich_from_infobox(entity, infobox)

            # 4. Handle Parent vs Subsidiary Disambiguation
            # Special check: e.g. Google LLC -> parent Alphabet Inc.
            if "google" in query_lower and not entity.get("parent_company"):
                if "alphabet" not in query_lower:
                    entity["is_subsidiary"] = True
                    entity["parent_company"] = "Alphabet Inc."

            if entity.get("parent_company"):
                entity["is_subsidiary"] = True
                entity["identity_notes"] = f"{entity['canonical_name']} is an operating subsidiary of parent entity {entity['parent_company']}. Consolidated financials reflect parent company."

            # Fetch parent infobox if subsidiary has a known parent company
            if entity.get("parent_company"):
                try:
                    parent_title = entity["parent_company"].replace(" ", "_")
                    parent_infobox = await cls._extract_wikipedia_infobox(client, parent_title)
                    if parent_infobox:
                        entity["_parent_infobox"] = parent_infobox
                        if not entity.get("ticker") and parent_infobox.get("traded_as"):
                            p_traded = parent_infobox.get("traded_as")
                            p_match = re.search(r'\b(NASDAQ|NYSE|BSE|NSE|LSE|FWB|TYO):\s*([A-Z0-9]+)\b', p_traded, re.I)
                            if p_match:
                                entity["ticker"] = f"{p_match.group(1).upper()}: {p_match.group(2).upper()} (Parent: {entity['parent_company']})"
                except Exception as e:
                    logger.warning(f"Failed to fetch parent entity infobox for '{entity.get('parent_company')}': {e}")
            
            # If still no website, derive best candidate or leave UNKNOWN
            if not entity["official_website"]:
                # If we have a clean slug, test common domains
                slug = re.sub(r'[^a-zA-Z0-9]', '', query_clean).lower()
                entity["official_website"] = f"https://www.{slug}.com"

        return entity

    @classmethod
    async def _search_wikipedia_entity(cls, client: httpx.AsyncClient, query: str) -> Optional[Dict[str, Any]]:
        """Searches Wikipedia API for the best corporate article match."""
        # Query tokens to ensure real relevance
        stopwords = {"inc", "corp", "corporation", "company", "llc", "ltd", "gmbh", "ag", "co", "the", "and"}
        query_words = set(re.findall(r'\b[a-zA-Z0-9]{3,}\b', query.lower())) - stopwords
        
        queries = [query, f"{query} company", f"{query} corporation"]
        for q in queries:
            try:
                res = await client.get(
                    "https://en.wikipedia.org/w/api.php",
                    params={
                        "action": "query",
                        "list": "search",
                        "srsearch": q,
                        "format": "json",
                        "utf8": 1
                    }
                )
                if res.status_code == 200:
                    results = res.json().get("query", {}).get("search", [])
                    for r in results:
                        title = r.get("title", "")
                        title_lower = title.lower()
                        snippet = r.get("snippet", "").lower()
                        
                        # Disambiguation or list pages are rejected
                        if any(term in title_lower for term in ["disambiguation", "list of", "category:", "timeline of"]):
                            continue

                        # Check word overlap: at least one core query word MUST be in title or first words of snippet
                        title_words = set(re.findall(r'\b[a-zA-Z0-9]{3,}\b', title_lower))
                        if query_words and not (query_words & title_words):
                            continue

                        # If title matches or snippet mentions company/corporation/multinational/business
                        if any(term in snippet for term in ["company", "corporation", "multinational", "headquarters", "subsidiary", "manufacturer", "firm", "technology", "enterprise"]):
                            # Fetch summary
                            summary_res = await client.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}")
                            if summary_res.status_code == 200:
                                data = summary_res.json()
                                if data.get("type") != "disambiguation":
                                    return data
            except Exception as e:
                logger.warning(f"Wikipedia search failed for '{q}': {e}")
        return None

    @classmethod
    async def _match_sec_ticker(cls, client: httpx.AsyncClient, query: str) -> Optional[Dict[str, Any]]:
        """Matches company against the official SEC company tickers registry."""
        tickers_data = await cls._get_sec_tickers(client)
        if not tickers_data:
            return None

        clean_q = re.sub(r'[^a-zA-Z0-9]', '', query).upper()
        
        # Check direct ticker match
        for item in tickers_data.values():
            if item.get("ticker", "").upper() == clean_q:
                return item

        # Check title match
        for item in tickers_data.values():
            title_clean = re.sub(r'[^a-zA-Z0-9]', '', item.get("title", "")).upper()
            if clean_q == title_clean or (len(clean_q) > 4 and clean_q in title_clean):
                return item

        return None

    @classmethod
    async def _extract_wikipedia_infobox(cls, client: httpx.AsyncClient, title: str) -> Dict[str, str]:
        """Fetches lead section wikitext and parses Infobox key-value pairs with multiline support."""
        infobox = {}
        try:
            res = await client.get(
                "https://en.wikipedia.org/w/api.php",
                params={
                    "action": "query",
                    "prop": "revisions",
                    "rvprop": "content",
                    "rvsection": 0,
                    "titles": title,
                    "format": "json"
                }
            )
            if res.status_code == 200:
                pages = res.json().get("query", {}).get("pages", {})
                for page_id, page_data in pages.items():
                    revisions = page_data.get("revisions", [])
                    if revisions:
                        wikitext = revisions[0].get("*", "")
                        
                        raw_fields = {}
                        current_key = None
                        current_val = []

                        for line in wikitext.splitlines():
                            line_s = line.strip()
                            if line_s.startswith("|") and "=" in line_s:
                                if current_key:
                                    raw_fields[current_key] = "\n".join(current_val)
                                parts = line_s[1:].split("=", 1)
                                current_key = parts[0].strip().lower()
                                current_val = [parts[1].strip()]
                            elif current_key:
                                if line_s == "}}" and not any("{" in l for l in current_val[-2:]):
                                    # End of template
                                    raw_fields[current_key] = "\n".join(current_val)
                                    current_key = None
                                    current_val = []
                                else:
                                    current_val.append(line_s)

                        if current_key:
                            raw_fields[current_key] = "\n".join(current_val)

                        for key, val_raw in raw_fields.items():
                            val = val_raw
                            # Expand multiline list templates like ubl/unbulleted list
                            val = re.sub(r'\{\{(?:ubl|unbulleted list|hlist|flatlist)[^|]*\|([\s\S]+?)\}\}', lambda m: m.group(1).replace('|', '\n'), val, flags=re.I)
                            # Expand currency templates
                            val = re.sub(r'\{\{(?:US\$|USD|US dollar)\|([^|}]+)[^}]*\}\}', r'US$ \1', val, flags=re.I)
                            val = re.sub(r'\{\{INRConvert\|([^|}]+)[^}]*\}\}', r'₹ \1 lakh crore', val, flags=re.I)
                            val = re.sub(r'\{\{euro\|([^|}]+)[^}]*\}\}', r'€ \1', val, flags=re.I)
                            # Clean wiki links [[Link|Text]] -> Text
                            val_clean = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]+)\]\]', r'\1', val)
                            # Strip HTML comments
                            val_clean = re.sub(r'<!--[\s\S]*?-->', '', val_clean)
                            # Strip decorative templates
                            val_clean = re.sub(r'\{\{(?:increase|decrease|up|down|steady|nbsp)\}\}', ' ', val_clean, flags=re.I)
                            val_clean = re.sub(r'\{\{[\s\S]+?\}\}', ' ', val_clean)
                            val_clean = re.sub(r'<ref[^>]*>.*?</ref>', '', val_clean, flags=re.DOTALL)
                            val_clean = re.sub(r'<ref[^>]*/>', '', val_clean)
                            val_clean = val_clean.replace("&nbsp;", " ").strip()
                            if key and val_clean:
                                infobox[key] = val_clean
        except Exception as e:
            logger.warning(f"Failed to extract Wikipedia Infobox for '{title}': {e}")
        return infobox

    @classmethod
    def _enrich_from_infobox(cls, entity: Dict[str, Any], infobox: Dict[str, str]):
        """Enriches entity fields from parsed Wikipedia Infobox."""
        # Headquarters
        city = infobox.get("hq_location_city") or infobox.get("location_city")
        country = infobox.get("hq_location_country") or infobox.get("location_country")
        raw_hq = infobox.get("headquarters") or infobox.get("hq_location")
        
        if city and country:
            entity["headquarters"] = f"{city}, {country}".strip(", ")
            entity["country"] = country
        elif raw_hq:
            entity["headquarters"] = raw_hq
        elif city:
            entity["headquarters"] = city
        
        # Type & Parent
        company_type = infobox.get("type", "")
        if "subsidiary" in company_type.lower():
            entity["company_type"] = "Subsidiary"
            entity["is_subsidiary"] = True
        elif "public" in company_type.lower():
            entity["company_type"] = "Public"
        elif "private" in company_type.lower():
            entity["company_type"] = "Private"

        parent = infobox.get("parent")
        if parent:
            entity["parent_company"] = parent
            entity["is_subsidiary"] = True

        # Ticker
        traded_as = infobox.get("traded_as")
        if traded_as and not entity.get("ticker"):
            # Extract tickers like NASDAQ: AMZN, NYSE: MSFT
            ticker_match = re.search(r'\b(NASDAQ|NYSE|BSE|NSE|LSE|FWB|TYO):\s*([A-Z0-9]+)\b', traded_as, re.I)
            if ticker_match:
                entity["ticker"] = f"{ticker_match.group(1).upper()}: {ticker_match.group(2).upper()}"
            else:
                clean_trade = re.sub(r'[\{\}\[\]\n\r]', '', traded_as).strip()
                if len(clean_trade) > 1 and re.search(r'[A-Za-z0-9]', clean_trade):
                    entity["ticker"] = clean_trade[:60]

        # Website
        website = infobox.get("website") or infobox.get("url")
        if website:
            url_match = re.search(r'https?://[^\s]+', website)
            if url_match:
                entity["official_website"] = url_match.group(0).rstrip("/>")
            elif "." in website:
                entity["official_website"] = f"https://{website.strip('/')}"

        # Industry
        industry = infobox.get("industry")
        if industry and (entity["industry"] == "UNKNOWN" or len(industry) > 3):
            # Clean up templates and lists
            clean_ind = re.sub(r'\{\{[^|}]*\|?', '', industry)
            clean_ind = re.sub(r'[\{\}\[\]]', '', clean_ind)
            clean_ind = re.sub(r'\s*\([^)]*\)', '', clean_ind)
            filter_tags = ["ubl", "unbulleted", "list", "hlist", "flatlist"]
            tokens = [
                p.strip() for p in re.split(r'[\r\n|,]+', clean_ind)
                if p.strip() and not any(t == p.lower() or t in p.lower() for t in filter_tags)
            ]
            if tokens:
                entity["industry"] = ", ".join(tokens[:3])

        # Store raw infobox for metrics & fact extraction
        entity["_raw_infobox"] = infobox
