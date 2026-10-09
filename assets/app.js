/* ============================================================
   知识库阅读外壳 app.js
   自动注入顶栏 / 侧边抽屉 / 进度条 / 上下篇 / 暗色模式
   支持 SPA 无刷新导航（点击侧边栏不闪烁）
   ============================================================ */
(function(){
  // 动态加载 manifest.js
  const s = document.createElement('script');
  s.src = '../assets/manifest.js';
  s.onload = init;
  document.head.appendChild(s);

  // 提前应用主题（避免闪烁）
  try{
    let t = localStorage.getItem('kb_theme');
    if(!t) t = matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', t);
  }catch(e){}

  function init(){
    const M = window.KB_MANIFEST;
    if(!M) return;

    let here = decodeURIComponent(location.pathname.split('/').slice(-2).join('/'));
    let curIdx = -1, prev = null, next = null, curCat = null;
    let flat = [];
    M.cats.forEach(c => c.arts.forEach(a => flat.push(a)));
    flat.forEach((a,i) => {
      if(a.u === here){ curIdx = i; prev = flat[i-1] || null; next = flat[i+1] || null; }
    });
    M.cats.forEach(c => c.arts.forEach(a => { if(a.u === here) curCat = c; }));

    /* ---------- 1. 进度条 ---------- */
    const prog = document.createElement('div');
    prog.id = 'kb-progress';
    document.body.appendChild(prog);

    /* ---------- 2. 顶栏 ---------- */
    const bar = document.createElement('header');
    bar.id = 'kb-topbar';
    bar.innerHTML = `
      <button class="kb-btn" id="kbMenuBtn" title="目录 (Alt+M)">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/></svg>
      </button>
      <a class="kb-btn" href="../index.html" title="返回首页" style="text-decoration:none">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="m12 19-7-7 7-7"/><path d="M19 12H5"/></svg>
      </a>
      <div id="kb-crumb">
        ${curCat ? `<span class="kb-cat">${curCat.icon} ${curCat.name}</span><span class="kb-sep">·</span>` : ''}
        <span class="kb-title">${document.title.replace('｜全栈技术知识库','')}</span>
      </div>
      <div class="kb-right">
        <button class="kb-btn" id="kbSearchBtn" title="搜索">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/><path d="M8 11h6"/></svg>
        </button>
        <button class="kb-btn" id="kbThemeBtn" title="切换主题">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
        </button>
      </div>`;
    document.body.appendChild(bar);

    /* ---------- 3. 侧边栏 ---------- */
    const mask = document.createElement('div');
    mask.id = 'kb-mask';
    document.body.appendChild(mask);

    const side = document.createElement('nav');
    side.id = 'kb-sidebar';
    side.innerHTML = `
      <div class="kb-side-search"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg><input id="kbSideSearch" placeholder="过滤文章…"></div>`;
    const listWrap = document.createElement('div');
    listWrap.id = 'kbSideList';
    side.appendChild(listWrap);
    document.body.appendChild(side);

    function renderSide(filter=''){
      listWrap.innerHTML = '';
      const q = filter.trim().toLowerCase();
      M.cats.forEach(c => {
        const arts = c.arts.filter(a => !q || a.t.toLowerCase().includes(q));
        if(q && arts.length === 0) return;
        const g = document.createElement('div');
        g.className = 'kb-cat-group';
        g.innerHTML = `<div class="kb-cat-name">${c.icon} ${c.name}</div>`;
        arts.forEach(a => {
          const item = document.createElement('a');
          item.className = 'kb-art' + (a.u === here ? ' active' : '');
          item.href = '../' + encodeURI(a.u);
          item.innerHTML = `<span class="dot ${a.d}"></span><span>${a.t}</span>`;
          g.appendChild(item);
        });
        listWrap.appendChild(g);
      });
    }
    renderSide();
    document.getElementById('kbSideSearch').addEventListener('input', e => renderSide(e.target.value));

    function openSide(){ side.classList.add('open'); mask.classList.add('show'); }
    function closeSide(){ side.classList.remove('open'); mask.classList.remove('show'); }
    document.getElementById('kbMenuBtn').onclick = () => side.classList.contains('open') ? closeSide() : openSide();
    document.getElementById('kbSearchBtn').onclick = openSide;
    mask.onclick = closeSide;

    function syncSidebarMode(){
      if(window.innerWidth >= 1280){
        side.classList.add('open');
        document.body.classList.add('kb-sidebar-on');
      } else {
        side.classList.remove('open');
        document.body.classList.remove('kb-sidebar-on');
      }
    }
    syncSidebarMode();
    let rt; window.addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(syncSidebarMode, 150); });

    /* ---------- 4. 暗色切换 ---------- */
    document.getElementById('kbThemeBtn').onclick = () => {
      const cur = document.documentElement.getAttribute('data-theme');
      const next = cur === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      try{ localStorage.setItem('kb_theme', next); }catch(e){}
    };

    /* ---------- 5. 上下篇 ---------- */
    function buildPager(){
      // 移除旧 pager
      const old = document.getElementById('kb-pager');
      if(old) old.remove();
      if(prev || next){
        const pager = document.createElement('div');
        pager.id = 'kb-pager';
        pager.innerHTML = `
          ${prev ? `<a class="prev" href="../${encodeURI(prev.u)}"><div class="dir">← 上一篇</div><div class="name">${prev.t}</div></a>` : '<span></span>'}
          ${next ? `<a class="next" href="../${encodeURI(next.u)}"><div class="dir">下一篇 →</div><div class="name">${next.t}</div></a>` : '<span></span>'}`;
        const footer = document.querySelector('footer');
        if(footer) document.body.insertBefore(pager, footer);
        else document.body.appendChild(pager);
      }
    }
    buildPager();

    /* ---------- 6. 滚动：进度条 ---------- */
    window.addEventListener('scroll', () => {
      const h = document.documentElement;
      const max = h.scrollHeight - h.clientHeight;
      prog.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + '%';
    }, {passive:true});

    /* ============================================================
       SPA 无刷新导航：拦截内部链接，只替换文章内容
       ============================================================ */
    const SHELL_IDS = ['kb-progress','kb-topbar','kb-sidebar','kb-mask','kb-pager'];

    function isShell(el){
      if(el.id && SHELL_IDS.includes(el.id)) return true;
      if(el.id === 'gloss-overlay') return true;
      return false;
    }

    // 重新初始化术语系统
    function reinitGlossary(){
      if(typeof window.initGlossary === 'function'){
        try{ window.initGlossary(); }catch(e){}
      }
    }

    // 更新当前文章索引
    function updateHere(path){
      here = path;
      curIdx = -1; prev = null; next = null; curCat = null;
      flat.forEach((a,i) => { if(a.u === here){ curIdx = i; prev = flat[i-1]||null; next = flat[i+1]||null; } });
      M.cats.forEach(c => c.arts.forEach(a => { if(a.u === here) curCat = c; }));
    }

    // 切换到新页面内容
    function navigateTo(url, pushUrl){
      // 保存侧边栏滚动位置
      const savedScroll = side.scrollTop;
      // 进度条动画
      prog.style.width = '20%';
      prog.style.transition = 'width 0.2s ease';

      fetch(url)
        .then(r => r.text())
        .then(html => {
          const doc = new DOMParser().parseFromString(html, 'text/html');
          // 更新标题
          document.title = doc.title;
          // 更新面包屑
          const crumb = document.getElementById('kb-crumb');
          if(crumb && curCat){
            crumb.innerHTML = `<span class="kb-cat">${curCat.icon} ${curCat.name}</span><span class="kb-sep">·</span><span class="kb-title">${doc.title.replace('｜全栈技术知识库','')}</span>`;
          }
          // 先把新内容准备好
          const temp = document.createElement('div');
          Array.from(doc.body.children).forEach(el => {
            if(isShell(el)) return;
            if(el.tagName === 'SCRIPT' && el.src && el.src.includes('app.js')) return;
            temp.appendChild(document.importNode(el, true));
          });
          // 一次性替换
          Array.from(document.body.children).forEach(el => {
            if(!isShell(el)) el.remove();
          });
          Array.from(temp.children).forEach(el => {
            document.body.appendChild(el);
            el.classList.add('kb-article-in');
          });
          // 更新侧边栏 active，保持滚动位置
          renderSide(document.getElementById('kbSideSearch').value);
          side.scrollTop = savedScroll;
          // 重建 pager
          buildPager();
          // 重新初始化术语
          reinitGlossary();
          // 滚动到顶
          window.scrollTo(0, 0);
          prog.style.width = '100%';
          setTimeout(() => { prog.style.width = '0'; }, 200);
        })
        .catch(() => {
          location.href = url;
        });
    }

    // 拦截所有内部链接点击（事件委托）
    document.addEventListener('click', e => {
      const a = e.target.closest('a');
      if(!a) return;
      const href = a.getAttribute('href');
      if(!href || href.startsWith('#') || href.startsWith('javascript:') || href.startsWith('http')) return;
      if(a.target === '_blank') return;
      // 只拦截 .html 链接
      if(!href.endsWith('.html')) return;
      // 首页链接不拦截（整页跳）
      if(href.includes('index.html')) return;

      e.preventDefault();
      // 计算相对路径
      const base = location.pathname.replace(/\/[^/]*$/, '/');
      const url = base + href;
      const path = decodeURIComponent(href.replace(/^\.\.\//,''));
      updateHere(path);
      navigateTo(url, href);
    });

    // 浏览器前进/后退
    window.addEventListener('popstate', e => {
      location.reload();
    });
  }
})();
