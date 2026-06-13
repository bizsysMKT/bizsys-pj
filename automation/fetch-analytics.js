#!/usr/bin/env node
/**
 * fetch-analytics.js
 *
 * GA4・Search Console APIから前月データを取得し
 * output/analysis/YYYY-MM-data.json に出力する。
 *
 * 前提：
 *   - automation/credentials/service-account.json が配置されていること
 *   - npm install googleapis が完了していること
 *
 * 実行方法：
 *   cd c:/Dev/bizsys-pj
 *   node automation/fetch-analytics.js
 */

const fs = require('fs');
const path = require('path');
const { google } = require('googleapis');

// ─── 設定 ───────────────────────────────────────────────

// GA4 プロパティID（例：properties/123456789）
// → GA4管理画面の「プロパティ設定」で確認できる数値IDを使う
const GA4_PROPERTY_ID = process.env.GA4_PROPERTY_ID || 'properties/531295406';

// Search Console サイトURL（登録時のURLと完全一致させる）
const SEARCH_CONSOLE_SITE_URL = process.env.SEARCH_CONSOLE_SITE_URL || 'https://bizsys.jp/';

// 出力ディレクトリ
const OUTPUT_DIR = path.join(__dirname, '..', 'output', 'analysis');

// ─── 日付ユーティリティ ──────────────────────────────────

/**
 * 前月の開始日・終了日を返す（JST基準）
 * @returns {{ startDate: string, endDate: string, period: string }}
 */
function getPreviousMonthRange() {
  const now = new Date();
  const year = now.getMonth() === 0 ? now.getFullYear() - 1 : now.getFullYear();
  const month = now.getMonth() === 0 ? 12 : now.getMonth(); // 前月（1〜12）

  const startDate = `${year}-${String(month).padStart(2, '0')}-01`;
  const lastDay = new Date(year, month, 0).getDate();
  const endDate = `${year}-${String(month).padStart(2, '0')}-${String(lastDay).padStart(2, '0')}`;
  const period = `${year}-${String(month).padStart(2, '0')}`;

  return { startDate, endDate, period };
}

// ─── 認証 ────────────────────────────────────────────────

function loadAuth() {
  const auth = new google.auth.GoogleAuth({
    keyFile: 'C:/Users/tk171/claude-work/google_credentials.json',
    scopes: [
      'https://www.googleapis.com/auth/analytics.readonly',
      'https://www.googleapis.com/auth/webmasters.readonly',
    ],
  });

  return auth;
}

// ─── GA4データ取得 ───────────────────────────────────────

async function fetchGA4Data(auth, startDate, endDate) {
  const analyticsData = google.analyticsdata({ version: 'v1beta', auth });

  // セッション数・ユーザー数
  const summaryRes = await analyticsData.properties.runReport({
    property: GA4_PROPERTY_ID,
    requestBody: {
      dateRanges: [{ startDate, endDate }],
      metrics: [
        { name: 'sessions' },
        { name: 'totalUsers' },
      ],
    },
  });

  const summaryRow = summaryRes.data.rows?.[0]?.metricValues ?? [];
  const sessions = parseInt(summaryRow[0]?.value ?? '0', 10);
  const users = parseInt(summaryRow[1]?.value ?? '0', 10);

  // ページ別PV（上位10件）
  const pageRes = await analyticsData.properties.runReport({
    property: GA4_PROPERTY_ID,
    requestBody: {
      dateRanges: [{ startDate, endDate }],
      dimensions: [{ name: 'pagePath' }],
      metrics: [{ name: 'screenPageViews' }],
      orderBys: [{ metric: { metricName: 'screenPageViews' }, desc: true }],
      limit: 10,
    },
  });

  const pageviewsByPage = (pageRes.data.rows ?? []).map(row => ({
    page: row.dimensionValues[0].value,
    pageviews: parseInt(row.metricValues[0].value, 10),
  }));

  // 流入元（チャネルグループ）
  const channelRes = await analyticsData.properties.runReport({
    property: GA4_PROPERTY_ID,
    requestBody: {
      dateRanges: [{ startDate, endDate }],
      dimensions: [{ name: 'sessionDefaultChannelGroup' }],
      metrics: [{ name: 'sessions' }],
    },
  });

  const channelMap = {};
  for (const row of channelRes.data.rows ?? []) {
    channelMap[row.dimensionValues[0].value] = parseInt(row.metricValues[0].value, 10);
  }

  const sessionsByChannel = {
    organic_search: channelMap['Organic Search'] ?? 0,
    social: channelMap['Organic Social'] ?? channelMap['Social'] ?? 0,
    direct: channelMap['Direct'] ?? 0,
  };

  return { sessions, users, pageviews_by_page: pageviewsByPage, sessions_by_channel: sessionsByChannel };
}

// ─── Search Console データ取得 ───────────────────────────

async function fetchSearchConsoleData(auth, startDate, endDate) {
  const searchconsole = google.searchconsole({ version: 'v1', auth });

  // クエリ別パフォーマンス（上位25件）
  const queryRes = await searchconsole.searchanalytics.query({
    siteUrl: SEARCH_CONSOLE_SITE_URL,
    requestBody: {
      startDate,
      endDate,
      dimensions: ['query'],
      rowLimit: 25,
      dataState: 'all',
    },
  });

  const queries = (queryRes.data.rows ?? []).map(row => ({
    query: row.keys[0],
    clicks: row.clicks ?? 0,
    impressions: row.impressions ?? 0,
    ctr: parseFloat((row.ctr ?? 0).toFixed(4)),
    position: parseFloat((row.position ?? 0).toFixed(1)),
  }));

  // ページ別パフォーマンス（上位25件）
  const pageRes = await searchconsole.searchanalytics.query({
    siteUrl: SEARCH_CONSOLE_SITE_URL,
    requestBody: {
      startDate,
      endDate,
      dimensions: ['page'],
      rowLimit: 25,
      dataState: 'all',
    },
  });

  const pages = (pageRes.data.rows ?? []).map(row => ({
    page: row.keys[0].replace(SEARCH_CONSOLE_SITE_URL.replace(/\/$/, ''), ''),
    clicks: row.clicks ?? 0,
    impressions: row.impressions ?? 0,
    ctr: parseFloat((row.ctr ?? 0).toFixed(4)),
    position: parseFloat((row.position ?? 0).toFixed(1)),
  }));

  return { queries, pages };
}

// ─── メイン ──────────────────────────────────────────────

async function main() {
  console.log('=== fetch-analytics.js 開始 ===');

  const { startDate, endDate, period } = getPreviousMonthRange();
  console.log(`対象期間: ${startDate} 〜 ${endDate}`);

  // 認証
  console.log('Service Account 認証中...');
  const auth = loadAuth();

  // データ取得
  console.log('GA4 データ取得中...');
  const ga4 = await fetchGA4Data(auth, startDate, endDate);

  console.log('Search Console データ取得中...');
  const searchConsole = await fetchSearchConsoleData(auth, startDate, endDate);

  // 出力
  const result = { period, ga4, search_console: searchConsole };

  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  const outputPath = path.join(OUTPUT_DIR, `${period}-data.json`);
  fs.writeFileSync(outputPath, JSON.stringify(result, null, 2), 'utf-8');

  console.log(`\n✓ 出力完了: ${outputPath}`);
  console.log(`  セッション数: ${ga4.sessions}`);
  console.log(`  ユーザー数:   ${ga4.users}`);
  console.log(`  検索クエリ数: ${searchConsole.queries.length}`);
  console.log('=== 完了 ===');
}

main().catch(err => {
  console.error('\n[ERROR]', err.message);
  process.exit(1);
});
