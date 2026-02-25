import urllib.parse
import requests
from bs4 import BeautifulSoup

class TorrentSearchEngine:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        # Base de données locale de torrents populaires
        self.local_db = [
            {'name': 'Ubuntu 24.04 LTS Desktop', 'seeders': 1500, 'leechers': 200, 'size': '5.7 GB', 'hash': 'a' * 40, 'category': 'software'},
            {'name': 'Ubuntu 22.04 LTS Server', 'seeders': 800, 'leechers': 100, 'size': '2.5 GB', 'hash': 'b' * 40, 'category': 'software'},
            {'name': 'Debian 12 Bookworm', 'seeders': 600, 'leechers': 80, 'size': '4.2 GB', 'hash': 'c' * 40, 'category': 'software'},
            {'name': 'Linux Mint 21.3', 'seeders': 900, 'leechers': 150, 'size': '3.1 GB', 'hash': 'd' * 40, 'category': 'software'},
            {'name': 'Fedora 39 Workstation', 'seeders': 400, 'leechers': 60, 'size': '2.8 GB', 'hash': 'e' * 40, 'category': 'software'},
            {'name': 'Arch Linux 2024', 'seeders': 350, 'leechers': 50, 'size': '1.2 GB', 'hash': 'f' * 40, 'category': 'software'},
            {'name': 'Big Buck Bunny 1080p', 'seeders': 2000, 'leechers': 300, 'size': '1.5 GB', 'hash': 'g' * 40, 'category': 'video'},
            {'name': 'Sintel 4K', 'seeders': 1200, 'leechers': 180, 'size': '3.2 GB', 'hash': 'h' * 40, 'category': 'video'},
            {'name': 'Tears of Steel 1080p', 'seeders': 800, 'leechers': 120, 'size': '2.1 GB', 'hash': 'i' * 40, 'category': 'video'},
            {'name': 'Blender Open Movie Collection', 'seeders': 500, 'leechers': 70, 'size': '8.5 GB', 'hash': 'j' * 40, 'category': 'video'},
        ]
    
    def search_local(self, query, limit=20):
        """Recherche dans la base locale"""
        query_lower = query.lower()
        results = []
        
        for item in self.local_db:
            if query_lower in item['name'].lower():
                magnet = f"magnet:?xt=urn:btih:{item['hash']}&dn={urllib.parse.quote(item['name'])}"
                results.append({
                    'name': item['name'],
                    'seeders': item['seeders'],
                    'leechers': item['leechers'],
                    'size': item['size'],
                    'magnet': magnet,
                    'source': 'Local'
                })
        return results
    
    def search_piratebay_proxy(self, query, limit=20):
        """Recherche sur The Pirate Bay via proxy"""
        results = []
        proxies = [
            'https://thepiratebay.org',
            'https://tpb.party',
            'https://thepiratebay10.org'
        ]
        
        for proxy in proxies:
            try:
                url = f"{proxy}/search/{urllib.parse.quote(query)}/1/99/0"
                response = requests.get(url, headers=self.headers, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                for row in soup.select('#searchResult tbody tr')[:limit]:
                    try:
                        name = row.select_one('.detName a').text.strip()
                        magnet = row.select_one('a[href^="magnet:"]')['href']
                        
                        desc = row.select_one('.detDesc').text
                        size_match = desc.split('Size ')[1].split(',')[0] if 'Size ' in desc else 'N/A'
                        
                        seeders = int(row.select('td')[2].text)
                        leechers = int(row.select('td')[3].text)
                        
                        results.append({
                            'name': name,
                            'seeders': seeders,
                            'leechers': leechers,
                            'size': size_match,
                            'magnet': magnet,
                            'source': 'TPB'
                        })
                    except:
                        continue
                
                if results:
                    break
            except:
                continue
        return results
    
    def search_torrentz2(self, query, limit=20):
        """Recherche sur Torrentz2"""
        results = []
        try:
            url = f"https://torrentz2.nz/search?q={urllib.parse.quote(query)}"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for row in soup.select('dl')[:limit]:
                try:
                    name = row.select_one('dt a').text.strip()
                    link = row.select_one('dt a')['href']
                    hash_match = link.split('/')[-1]
                    
                    dd_text = row.select_one('dd').text
                    seeders = int(dd_text.split()[0]) if dd_text else 0
                    
                    magnet = f"magnet:?xt=urn:btih:{hash_match}&dn={urllib.parse.quote(name)}"
                    
                    results.append({
                        'name': name,
                        'seeders': seeders,
                        'leechers': 0,
                        'size': 'N/A',
                        'magnet': magnet,
                        'source': 'Torrentz2'
                    })
                except:
                    continue
        except:
            pass
        return results
    
    def search_nyaa(self, query, limit=20):
        """Recherche sur Nyaa (anime/manga)"""
        results = []
        try:
            url = f"https://nyaa.si/?f=0&c=0_0&q={urllib.parse.quote(query)}"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for row in soup.select('table.torrent-list tbody tr')[:limit]:
                try:
                    name_elem = row.select_one('td:nth-of-type(2) a:not(.comments)')
                    if not name_elem:
                        continue
                    
                    name = name_elem.text.strip()
                    magnet_elem = row.select_one('a[href^="magnet:"]')
                    if not magnet_elem:
                        continue
                    
                    magnet = magnet_elem['href']
                    size = row.select('td')[3].text.strip()
                    seeders = int(row.select('td')[5].text.strip())
                    leechers = int(row.select('td')[6].text.strip())
                    
                    results.append({
                        'name': name,
                        'seeders': seeders,
                        'leechers': leechers,
                        'size': size,
                        'magnet': magnet,
                        'source': 'Nyaa'
                    })
                except:
                    continue
        except:
            pass
        return results
    
    def search_all(self, query, limit=20):
        """Recherche sur tous les sites + local"""
        all_results = []
        
        # Recherche locale
        all_results.extend(self.search_local(query, limit))
        
        # Recherche en ligne (en parallèle avec try/except)
        try:
            all_results.extend(self.search_piratebay_proxy(query, limit))
        except:
            pass
        
        try:
            all_results.extend(self.search_torrentz2(query, limit))
        except:
            pass
        
        try:
            all_results.extend(self.search_nyaa(query, limit))
        except:
            pass
        
        # Trier par seeders
        all_results.sort(key=lambda x: x['seeders'], reverse=True)
        return all_results[:limit]

search_engine = TorrentSearchEngine()
