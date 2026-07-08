// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: 'https://bizsys.jp',
  base: '/',

  // URLの正規形を「末尾スラッシュあり」に統一する（2026-07-08）。
  // これを指定しないと /blog/foo と /blog/foo/ が別URLとして二重インデックスされ、
  // canonical・内部リンク・リダイレクト先の不一致でSEO評価が分散する。
  // build.format: 'directory' は /blog/foo/index.html を生成し、GitHub Pages配信と整合する。
  // @astrojs/sitemap もこの設定に従い、末尾スラッシュ付きURLでsitemapを出力する。
  trailingSlash: 'always',
  build: {
    format: 'directory',
  },

  integrations: [sitemap()],
  // ブログ記事のスラッグを日付なしへ統一した際の旧URL→新URLリダイレクト（2026-06-30）。
  // GitHub Pages配信のため静的リダイレクト（meta refresh + canonical）が生成される。
  // インデックス済み/被リンクされた旧URL（/blog/YYYY-MM-DD-スラッグ）を新URLへ転送する。
  // リダイレクト先は必ず末尾スラッシュ付き（trailingSlash:'always'・canonical と一致させる）。
  // 先がスラッシュなしだと、リダイレクトstubのcanonicalがスラッシュなしURLを主張し、
  // 実ページのcanonical（スラッシュあり）と食い違って二重インデックスの原因になる（2026-07-08）。
  redirects: {
    '/blog/2026-04-10-excel-zaiko-kanri-genkai': '/blog/excel-zaiko-kanri-genkai/',
    '/blog/2026-04-11-chusho-dx-hajimekata': '/blog/chusho-dx-hajimekata/',
    '/blog/2026-04-11-excel-dakkyaku-dekinai-riyuu': '/blog/excel-dakkyaku-dekinai-riyuu/',
    '/blog/2026-05-01-gyomu-jidoka-kawaru': '/blog/gyomu-jidoka-kawaru/',
    '/blog/2026-05-01-gyomu-zokuninoka-kiken': '/blog/gyomu-zokuninoka-kiken/',
    '/blog/2026-05-01-system-hatchuu-checklist': '/blog/system-hatchuu-checklist/',
    '/blog/2026-05-01-system-ka-merit': '/blog/system-ka-merit/',
    '/blog/2026-05-01-system-kaisha-erabi': '/blog/system-kaisha-erabi/',
    '/blog/2026-05-01-system-tsukutte-owari': '/blog/system-tsukutte-owari/',
    '/blog/2026-05-29-excel-dakkyaku-first-step': '/blog/excel-dakkyaku-first-step/',
    '/blog/2026-06-13-nippo-jidoka-houhou': '/blog/nippo-jidoka-houhou/',
    '/blog/2026-06-13-zokuninoka-fusegu-first-step': '/blog/zokuninoka-fusegu-first-step/',
    '/blog/2026-06-14-excel-system-ka-hiyou': '/blog/excel-system-ka-hiyou/',
    '/blog/2026-06-15-excel-shukei-sagyou-herasu': '/blog/excel-shukei-sagyou-herasu/',
    '/blog/2026-06-15-gyomu-system-jisaku-hikaku': '/blog/gyomu-system-jisaku-hikaku/',
    '/blog/2026-06-16-excel-juchu-kanri-miss': '/blog/excel-juchu-kanri-miss/',
    '/blog/2026-06-16-zaiko-kanri-ai-jisaku': '/blog/zaiko-kanri-ai-jisaku/',
    '/blog/2026-06-17-excel-system-ikou-nagare': '/blog/excel-system-ikou-nagare/',
    '/blog/2026-06-17-kokyaku-kanri-ai-jisaku': '/blog/kokyaku-kanri-ai-jisaku/',
    '/blog/2026-06-18-excel-system-ka-junbi': '/blog/excel-system-ka-junbi/',
    '/blog/2026-06-19-unsougyou-haisha-system': '/blog/unsougyou-haisha-system/',
    '/blog/2026-06-20-seizougyou-seisan-system': '/blog/seizougyou-seisan-system/',
    '/blog/2026-06-21-unsougyou-sharyou-kanri': '/blog/unsougyou-sharyou-kanri/',
    '/blog/2026-06-22-genka-kanri-system': '/blog/genka-kanri-system/',
    '/blog/2026-06-23-unsougyou-seikyuu-system': '/blog/unsougyou-seikyuu-system/',
    '/blog/2026-06-24-seizougyou-zaiko-kanri': '/blog/seizougyou-zaiko-kanri/',
    '/blog/2026-06-25-kensetsu-genka-kanri': '/blog/kensetsu-genka-kanri/',
    '/blog/2026-06-26-barcode-zaiko-kanri': '/blog/barcode-zaiko-kanri/',
    '/blog/2026-06-27-juchu-kanri-system': '/blog/juchu-kanri-system/',
    '/blog/2026-06-28-eigyou-nippo-system': '/blog/eigyou-nippo-system/',
    '/blog/2026-06-29-shokuhin-genka-kanri': '/blog/shokuhin-genka-kanri/',
    '/blog/2026-06-30-system-yoken-teigi': '/blog/system-yoken-teigi/',
    '/blog/2026-07-01-unsougyou-tenko-system': '/blog/unsougyou-tenko-system/',

    // 過去に存在し削除済みのページ（検索インデックスに残っておりクリック流入が404になっていた）。
    // トップへ転送する（2026-07-05）。
    '/tools': '/',
    '/faq': '/',
    '/about': '/',
  },
});
