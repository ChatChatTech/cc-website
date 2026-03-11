// Firecrawl research scraper - gather industry insights for article generation
import { FirecrawlAppV1 } from '@mendable/firecrawl-js';
import fs from 'fs';

const app = new FirecrawlAppV1({ apiKey: 'fc-82416113727a473792e07addfdadced0' });

const urls = [
  'https://www.gov.cn/zhengce/content/202312/content_6923076.htm',
  'https://www.secrss.com/articles/63000',
  'https://www.thepaper.cn/newsDetail_forward_26153851',
  'https://36kr.com/p/2616268291463424',
  'https://www.infoq.cn/article/privacy-computing-2024-trends',
];

async function scrapeAll() {
  const results = [];
  for (const url of urls) {
    try {
      console.log(`Scraping: ${url}`);
      const result = await app.scrapeUrl(url, { formats: ['markdown'] });
      if (result.success) {
        results.push({
          url,
          title: result.metadata?.title || '',
          content: (result.markdown || '').slice(0, 4000),
        });
        console.log(`  OK: ${result.metadata?.title || 'no title'} (${(result.markdown||'').length} chars)`);
      } else {
        console.log(`  SKIP: failed`);
      }
    } catch (e) {
      console.log(`  ERR: ${e.message?.slice(0, 120)}`);
    }
  }
  fs.writeFileSync('research_scrape.json', JSON.stringify(results, null, 2));
  console.log(`\nSaved ${results.length} results to research_scrape.json`);
}

scrapeAll();
