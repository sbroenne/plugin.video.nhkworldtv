import { test, expect } from '@playwright/test';
import * as fs from 'fs';

test('Extract NHK API configuration', async ({ page }) => {
  console.log('Navigating to NHK World website...');
  
  // Go to the NHK World homepage
  await page.goto('https://www3.nhk.or.jp/nhkworld/en/ondemand/', { 
    waitUntil: 'networkidle',
    timeout: 60000
  });

  // Try to find and download the API configuration file
  const apiUrls = [
    'https://www3.nhk.or.jp/nhkworld/assets/api_sdk/api2.json',
    'https://www3.nhk.or.jp/nhkworld/assets/api_sdk/api.json',
    'https://www3.nhk.or.jp/nhkworld/common/api.json'
  ];

  for (const apiUrl of apiUrls) {
    console.log(`Trying to fetch API from: ${apiUrl}`);
    try {
      const response = await page.request.get(apiUrl);
      if (response.ok()) {
        const apiData = await response.json();
        console.log(`Successfully fetched API from: ${apiUrl}`);
        console.log('API Data:', JSON.stringify(apiData, null, 2));
        
        // Save to file
        fs.writeFileSync(
          './plugin.video.nhkworldtv/lib/api_current.json',
          JSON.stringify(apiData, null, 2)
        );
        console.log('Saved API data to api_current.json');
        break;
      } else {
        console.log(`Failed to fetch from ${apiUrl}: ${response.status()}`);
      }
    } catch (error) {
      console.log(`Error fetching ${apiUrl}:`, error);
    }
  }

  // Look for API-related JavaScript files in the page
  console.log('\nSearching for API-related JavaScript files...');
  const scripts = await page.locator('script[src]').all();
  const scriptUrls: string[] = [];
  
  for (const script of scripts) {
    const src = await script.getAttribute('src');
    if (src && (src.includes('api') || src.includes('player') || src.includes('config'))) {
      scriptUrls.push(src.startsWith('http') ? src : `https://www3.nhk.or.jp${src}`);
    }
  }
  
  console.log('Found API-related scripts:', scriptUrls);

  // Try to fetch and analyze each script
  for (const scriptUrl of scriptUrls.slice(0, 5)) { // Limit to first 5 to avoid too many requests
    try {
      console.log(`\nFetching script: ${scriptUrl}`);
      const response = await page.request.get(scriptUrl);
      if (response.ok()) {
        const scriptContent = await response.text();
        
        // Look for API endpoints
        const apiPatterns = [
          /nwapi\.nhk\.jp[^"'\s]*/g,
          /nhkworld\/\w+\/v\d+[^"'\s]*/g,
          /api[^"'\s]*\.json/g,
          /"api":\s*\{[^}]+\}/g
        ];

        for (const pattern of apiPatterns) {
          const matches = scriptContent.match(pattern);
          if (matches && matches.length > 0) {
            console.log(`Found API patterns in ${scriptUrl}:`, [...new Set(matches)].slice(0, 10));
          }
        }
      }
    } catch (error) {
      console.log(`Error fetching script ${scriptUrl}:`, error);
    }
  }

  // Check if the page makes API calls during loading
  console.log('\nMonitoring network requests for API calls...');
  const apiCalls: { url: string; status: number }[] = [];
  
  page.on('response', response => {
    const url = response.url();
    if (url.includes('nwapi.nhk.jp') || url.includes('/api/') || url.includes('.json')) {
      apiCalls.push({ url, status: response.status() });
    }
  });

  // Navigate to trigger API calls
  await page.goto('https://www3.nhk.or.jp/nhkworld/en/ondemand/', { 
    waitUntil: 'networkidle',
    timeout: 60000
  });

  // Wait a bit for any delayed API calls
  await page.waitForTimeout(3000);

  console.log('\nAPI calls detected:');
  apiCalls.forEach(call => {
    console.log(`  ${call.status} - ${call.url}`);
  });

  // Try to extract API base URL and version from page content
  const pageContent = await page.content();
  const apiBasePattern = /nwapi\.nhk\.jp\/nhkworld\/[^"'\s]*/g;
  const apiMatches = pageContent.match(apiBasePattern);
  
  if (apiMatches) {
    console.log('\nAPI URLs found in page content:', [...new Set(apiMatches)]);
  }
});

test('Check specific NHK API endpoints', async ({ page }) => {
  const endpoints = [
    'https://nwapi.nhk.jp/nhkworld/vodesdlist/v7b/mostwatch/all/en/all/all.json',
    'https://nwapi.nhk.jp/nhkworld/epg/v7b/world/now.json',
    'https://www3.nhk.or.jp/nhkworld/assets/api_sdk/api2.json',
    'https://www3.nhk.or.jp/nhkworld/common/assets/news/config/en.json'
  ];

  for (const endpoint of endpoints) {
    console.log(`\nChecking endpoint: ${endpoint}`);
    try {
      const response = await page.request.get(endpoint);
      console.log(`Status: ${response.status()}`);
      console.log(`Headers:`, response.headers());
      
      if (response.ok()) {
        const data = await response.json();
        console.log(`Response preview:`, JSON.stringify(data).substring(0, 200));
      } else if (response.status() === 403) {
        console.log('❌ 403 Forbidden - Endpoint may require authentication or different headers');
      }
    } catch (error) {
      console.log(`Error:`, error);
    }
  }
});
