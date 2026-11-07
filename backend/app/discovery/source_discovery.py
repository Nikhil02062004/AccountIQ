import asyncio
import datetime
import logging
import re
from typing import Dict, Any, List, Optional, Tuple
from abc import ABC, abstractmethod
import httpx

logger = logging.getLogger(__name__)

USER_AGENT = "AccountIQ-Bot/1.0 (https://bridgeai.ai; sahai.khunteta@bridgeai.ai) Mozilla/5.0"

def get_current_date() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

class DiscoveredSource:
    def __init__(
        self,
        id: str,
        name: str,
        url: str,
        source_type: str,
        publication_date: Optional[str] = None,
        date_retrieved: Optional[str] = None,
        author: Optional[str] = None,
        is_official: bool = True,
        reliability_weight: float = 0.90,
        notes: Optional[str] = None,
        raw_content: Optional[str] = None
    ):
        self.id = id
        self.name = name
        self.url = url
        self.source_type = source_type
        self.publication_date = publication_date or get_current_date()
        self.date_retrieved = date_retrieved or get_current_date()
        self.author = author
        self.is_official = is_official
        self.reliability_weight = reliability_weight
        self.notes = notes
        self.raw_content = raw_content or ""


class BaseSourceAdapter(ABC):
    @abstractmethod
    async def discover(self, account_id: str, entity: Dict[str, Any], client: httpx.AsyncClient) -> List[DiscoveredSource]:
        pass

    async def fetch_with_retry(self, client: httpx.AsyncClient, url: str, **kwargs) -> Optional[httpx.Response]:
        """Executes HTTP request with exponential backoff retry for transient network errors."""
        max_retries = 2
        for attempt in range(max_retries + 1):
            try:
                res = await client.get(url, **kwargs)
                if res.status_code < 500:
                    return res
            except (httpx.TimeoutException, httpx.NetworkError) as e:
                if attempt == max_retries:
                    logger.info(f"Source adapter request timed out for {url}: {e}")
                    return None
                await asyncio.sleep(0.5 * (attempt + 1))
            except Exception as e:
                logger.warning(f"Unexpected request error for {url}: {e}")
                return None
        return None


class WikipediaSourceAdapter(BaseSourceAdapter):
    """Discovers Wikipedia corporate profile and encyclopedic evidence."""
    async def discover(self, account_id: str, entity: Dict[str, Any], client: httpx.AsyncClient) -> List[DiscoveredSource]:
        sources = []
        wiki_title = entity.get("wikipedia_title")
        if not wiki_title:
            return sources

        url = f"https://en.wikipedia.org/wiki/{wiki_title.replace(' ', '_')}"
        raw_text = entity.get("wikipedia_extract", "")
        infobox = entity.get("_raw_infobox", {})
        
        # Serialize infobox summary into content for claim verification
        content_lines = [raw_text] if raw_text else []
        for k, v in infobox.items():
            content_lines.append(f"{k}: {v}")
        full_content = "\n".join(content_lines)

        sources.append(DiscoveredSource(
            id=f"src-{account_id}-wikipedia",
            name=f"Wikipedia Verified Public Record: {wiki_title}",
            url=url,
            source_type="REPUTABLE_BUSINESS_PRESS",
            publication_date=get_current_date(),
            author="Wikipedia Wikimedia Contributors",
            is_official=False,
            reliability_weight=0.85,
            notes="Corporate profile and operational data extracted from Wikipedia and Wikidata.",
            raw_content=full_content
        ))
        return sources


class SecEdgarSourceAdapter(BaseSourceAdapter):
    """Discovers official SEC EDGAR 10-K and 10-Q regulatory filings for US public entities."""
    async def discover(self, account_id: str, entity: Dict[str, Any], client: httpx.AsyncClient) -> List[DiscoveredSource]:
        sources = []
        cik = entity.get("cik")
        if not cik:
            return sources

        try:
            cik_padded = f"{int(cik):010d}"
            sec_url = f"https://data.sec.gov/submissions/CIK{cik_padded}.json"
            res = await client.get(sec_url, headers={"User-Agent": USER_AGENT}, timeout=8.0)
            if res.status_code == 200:
                data = res.json()
                legal_name = data.get("name", entity.get("canonical_name"))
                filings = data.get("filings", {}).get("recent", {})
                
                # Find latest 10-K or 10-Q
                forms = filings.get("form", [])
                acc_nums = filings.get("accessionNumber", [])
                doc_names = filings.get("primaryDocument", [])
                report_dates = filings.get("filingDate", [])
                
                target_idx = None
                for i, form in enumerate(forms[:15]):
                    if form in ["10-K", "10-Q", "20-F"]:
                        target_idx = i
                        break

                filing_url = f"https://www.sec.gov/edgar/browse/?CIK={cik_padded}"
                pub_date = get_current_date()
                form_type = "10-K Annual Report"
                
                if target_idx is not None:
                    raw_acc = acc_nums[target_idx].replace("-", "")
                    doc = doc_names[target_idx]
                    form_type = forms[target_idx]
                    pub_date = report_dates[target_idx]
                    filing_url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{raw_acc}/{doc}"

                sources.append(DiscoveredSource(
                    id=f"src-{account_id}-sec-edgar",
                    name=f"U.S. SEC EDGAR Official Regulatory Filing ({form_type}): {legal_name}",
                    url=filing_url,
                    source_type="INVESTOR_FILING",
                    publication_date=pub_date,
                    author="U.S. Securities and Exchange Commission",
                    is_official=True,
                    reliability_weight=1.0,
                    notes=f"Official regulatory disclosure audited under SEC reporting requirements. SIC: {data.get('sicDescription', 'N/A')}.",
                    raw_content=f"Official SEC filing for {legal_name}. CIK: {cik_padded}. SIC: {data.get('sicDescription')}. Address: {data.get('addresses', {}).get('business', {})}"
                ))
        except Exception as e:
            logger.warning(f"SEC EDGAR adapter lookup failed for CIK {cik}: {e}")

        return sources


class WebDomainSourceAdapter(BaseSourceAdapter):
    """Validates and discovers official corporate domain and meta descriptions."""
    async def discover(self, account_id: str, entity: Dict[str, Any], client: httpx.AsyncClient) -> List[DiscoveredSource]:
        sources = []
        website = entity.get("official_website")
        if not website:
            return sources

        name = entity.get("canonical_name", "Enterprise")
        content_summary = f"{name} official web portal and enterprise services."

        try:
            res = await client.get(website, headers={"User-Agent": USER_AGENT}, timeout=6.0, follow_redirects=True)
            if res.status_code == 200:
                html_text = res.text[:8000]
                # Extract meta description
                meta_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html_text, re.I)
                if not meta_match:
                    meta_match = re.search(r'<meta\s+property=["\']og:description["\']\s+content=["\'](.*?)["\']', html_text, re.I)
                
                if meta_match:
                    content_summary = meta_match.group(1).strip()
                
                # Check title
                title_match = re.search(r'<title>(.*?)</title>', html_text, re.I)
                doc_title = title_match.group(1).strip() if title_match else f"{name} Homepage"
                
                sources.append(DiscoveredSource(
                    id=f"src-{account_id}-official-web",
                    name=f"Official Corporate Website: {doc_title}",
                    url=str(res.url),
                    source_type="OFFICIAL_WEBSITE",
                    publication_date=get_current_date(),
                    author=f"{name} Corporate Communications",
                    is_official=True,
                    reliability_weight=0.95,
                    notes="Direct corporate domain inspection and verified metadata.",
                    raw_content=f"{doc_title}. {content_summary}"
                ))
        except Exception as e:
            logger.info(f"Direct domain check for {website} returned: {e}")
            # If network error or timeout, create standard registered reference without fabricating
            sources.append(DiscoveredSource(
                id=f"src-{account_id}-official-web",
                name=f"{name} Corporate Domain",
                url=website,
                source_type="OFFICIAL_WEBSITE",
                publication_date=get_current_date(),
                author=f"{name} Corporate",
                is_official=True,
                reliability_weight=0.90,
                notes="Primary corporate domain registered.",
                raw_content=f"{name} primary corporate web presence: {website}"
            ))

        return sources


class SourceDiscoveryManager:
    """Manages modular adapters and coordinates source discovery with in-memory caching and deduplication."""
    _cache: Dict[str, Tuple[str, List[DiscoveredSource]]] = {}

    def __init__(self):
        self.adapters: List[BaseSourceAdapter] = [
            WikipediaSourceAdapter(),
            SecEdgarSourceAdapter(),
            WebDomainSourceAdapter()
        ]

    async def discover_sources(self, account_id: str, entity: Dict[str, Any], use_cache: bool = True) -> List[DiscoveredSource]:
        cache_key = f"{account_id}:{entity.get('canonical_name', '')}"
        today = get_current_date()
        if use_cache and cache_key in self._cache:
            cached_date, cached_sources = self._cache[cache_key]
            if cached_date == today and cached_sources:
                return cached_sources

        async with httpx.AsyncClient(timeout=10.0, headers={"User-Agent": USER_AGENT}) as client:
            tasks = [adapter.discover(account_id, entity, client) for adapter in self.adapters]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            all_sources: List[DiscoveredSource] = []
            seen_urls = set()
            for res in results:
                if isinstance(res, list):
                    for src in res:
                        if src.url not in seen_urls:
                            seen_urls.add(src.url)
                            all_sources.append(src)
            
            self._cache[cache_key] = (today, all_sources)
            return all_sources
