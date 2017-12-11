steps:

1. download seeds, aka search results (manual)
2. harvest title pages from seeds: `python title_urls_from_seeds.py [search pages] > ../data/title_urls/seeds'
3. scrape title pages: `python title_pages_from_urls.py ../data/title_urls/seeds ../data/title_pages/`
4. pull out subtitle pages from title pages: `python title_pages_to_subtitle_page_urls.py ../data/title_pages/ > ../data/subtitle_pages/sub_pages.txt`
5. scrape .srt files: `python dl_subs_for_langs.py ../data/subtitle_pages/sub_pages.txt ../data/subs english japanese`
