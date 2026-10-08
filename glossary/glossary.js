/* ============================================================
 * 全栈技术栈详解 · 术语系统引擎
 * 功能：
 *   1. 扫描正文文本节点，把术语库中的词自动加上 .gloss-term 标注
 *   2. 点击标注词 → 弹出术语详情 modal
 *   3. 在 <main> 末尾生成"本页术语表"模块
 * 依赖：glossary-data.js 中的 window.GLOSSARY
 * ============================================================ */
(function () {
  'use strict';

  var GLOSSARY = window.GLOSSARY || {};
  // 按长度降序，避免短词先匹配吃掉长词（如 "闭包" vs "闭包捕获"）
  var TERMS = Object.keys(GLOSSARY).sort(function (a, b) { return b.length - a.length; });
  if (!TERMS.length) return;

  // 跳过这些标签内部（不标注代码、链接、已标注词、SVG 等）
  var SKIP_TAGS = {
    CODE: 1, PRE: 1, SCRIPT: 1, STYLE: 1, SVG: 1, NOSCRIPT: 1,
    A: 1, BUTTON: 1, TEXTAREA: 1, INPUT: 1, SELECT: 1,
    H1: 1, H2: 1, H3: 1, H4: 1, H5: 1,
    'GLOSS-TERM': 1
  };

  var usedTerms = {}; // 本页实际用到的术语

  // ---------- 1. 构建匹配正则 ----------
  // 转义正则特殊字符
  function escapeRegExp(s) {
    return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }
  var pattern = new RegExp('(' + TERMS.map(escapeRegExp).join('|') + ')', 'g');

  // ---------- 2. 递归遍历文本节点 ----------
  function annotateNode(root) {
    // 只处理正文区域：main 里的 section.card，但排除 toc/hero/nav/footer
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode: function (node) {
        // 空文本跳过
        if (!node.nodeValue || !node.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
        // 检查父链是否在跳过的标签里
        var el = node.parentElement;
        while (el) {
          if (el === root) break;
          if (SKIP_TAGS[el.tagName]) return NodeFilter.FILTER_REJECT;
          if (el.classList && (el.classList.contains('gloss-term') ||
                               el.classList.contains('toc') ||
                               el.classList.contains('hero') ||
                               el.classList.contains('doc-nav'))) return NodeFilter.FILTER_REJECT;
          el = el.parentElement;
        }
        // 文本里必须至少命中一个术语
        return pattern.test(node.nodeValue) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
      }
    });

    var nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);

    nodes.forEach(function (textNode) {
      replaceText(textNode);
    });
  }

  // ---------- 3. 把单个文本节点里的术语替换为 span ----------
  function replaceText(textNode) {
    var text = textNode.nodeValue;
    var frag = document.createDocumentFragment();
    var lastIndex = 0;
    var m;
    pattern.lastIndex = 0;

    while ((m = pattern.exec(text)) !== null) {
      // 前面的普通文本
      if (m.index > lastIndex) {
        frag.appendChild(document.createTextNode(text.slice(lastIndex, m.index)));
      }
      var term = m[0];
      var span = document.createElement('span');
      span.className = 'gloss-term';
      span.setAttribute('data-term', term);
      span.textContent = term;
      frag.appendChild(span);
      usedTerms[term] = true;
      lastIndex = m.index + term.length;
    }
    // 尾部剩余
    if (lastIndex < text.length) {
      frag.appendChild(document.createTextNode(text.slice(lastIndex)));
    }
    textNode.parentNode.replaceChild(frag, textNode);
  }

  // ---------- 4. 弹窗 ----------
  var overlay = null;
  function openModal(term) {
    var info = GLOSSARY[term];
    if (!info) return;

    closeModal(); // 先关已有的

    overlay = document.createElement('div');
    overlay.className = 'gloss-overlay';
    overlay.innerHTML =
      '<div class="gloss-modal" role="dialog" aria-modal="true" aria-label="' + term + '">' +
        '<div class="gloss-modal-head">' +
          '<div>' +
            '<div class="gloss-modal-title">' + term +
              (info.en ? '<span class="gloss-modal-en">' + info.en + '</span>' : '') +
            '</div>' +
            (info.cat ? '<span class="gloss-modal-cat">' + info.cat + '</span>' : '') +
          '</div>' +
          '<button class="gloss-modal-close" aria-label="关闭">×</button>' +
        '</div>' +
        '<div class="gloss-modal-body">' +
          (info.short ? '<div class="gloss-short">' + info.short + '</div>' : '') +
          '<div class="gloss-detail">' + (info.detail || '') + '</div>' +
        '</div>' +
      '</div>';

    overlay.addEventListener('click', function (e) {
      if (e.target === overlay || e.target.closest('.gloss-modal-close')) closeModal();
    });
    document.addEventListener('keydown', escClose);
    document.body.appendChild(overlay);
  }
  function closeModal() {
    if (overlay) {
      overlay.remove();
      overlay = null;
      document.removeEventListener('keydown', escClose);
    }
  }
  function escClose(e) {
    if (e.key === 'Escape') closeModal();
  }

  // ---------- 5. 生成底部术语表 ----------
  function buildIndex() {
    var terms = Object.keys(usedTerms).sort(function (a, b) {
      // 先按分类，再按术语名
      var ca = GLOSSARY[a].cat || '其他';
      var cb = GLOSSARY[b].cat || '其他';
      if (ca !== cb) return ca.localeCompare(cb, 'zh');
      return a.localeCompare(b, 'zh');
    });
    if (!terms.length) return;

    var main = document.querySelector('main');
    if (!main) return;

    var box = document.createElement('section');
    box.className = 'gloss-index';
    box.id = 'gloss-index';
    box.innerHTML =
      '<div class="gloss-index-head">' +
        '<div class="gloss-index-title">本页术语表</div>' +
        '<div class="gloss-index-count">共 ' + terms.length + ' 个 · 点击任意词查看详细解释</div>' +
      '</div>' +
      '<div class="gloss-index-grid">' +
        terms.map(function (t) {
          var info = GLOSSARY[t];
          return '<div class="gloss-index-item" data-term="' + t + '">' +
                   '<span class="term-name">' + t + '</span>' +
                   (info.en ? '<span class="term-en">' + info.en + '</span>' : '') +
                 '</div>';
        }).join('') +
      '</div>';

    main.appendChild(box);

    // 术语表内项点击也开 modal
    box.addEventListener('click', function (e) {
      var item = e.target.closest('.gloss-index-item');
      if (item) openModal(item.getAttribute('data-term'));
    });
  }

  // ---------- 6. 事件委托：点击正文术语 ----------
  document.addEventListener('click', function (e) {
    var t = e.target.closest('.gloss-term');
    if (t) openModal(t.getAttribute('data-term'));
  });

  // ---------- 启动 ----------
  function init() {
    // 扫描 main 下所有 section.card
    var containers = document.querySelectorAll('main section.card');
    if (!containers.length) containers = [document.querySelector('main')];
    containers.forEach(function (c) { annotateNode(c); });
    buildIndex();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
