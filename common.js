// 悬浮导航显示/隐藏 + 修复目录树 + 改造左右分栏布局
document.addEventListener('DOMContentLoaded', function() {
  // ===== PC端：改造左右分栏布局 =====
  if (window.innerWidth > 1023) {
    const topNav = document.querySelector('.doc-nav.top');
    const toc = document.querySelector('nav.toc, .toc');
    const container = document.querySelector('.container');
    
    if (toc && container) {
      // 创建主包装器
      const mainWrapper = document.createElement('div');
      mainWrapper.className = 'main-wrapper';
      
      // 把toc和container移到mainWrapper里
      container.parentNode.insertBefore(mainWrapper, container);
      mainWrapper.appendChild(toc);
      mainWrapper.appendChild(container);
      
      // 给toc加类名
      toc.classList.add('sidebar-toc');
      
      // 重新生成单列表目录
      const ol = toc.querySelector('ol');
      if (ol) {
        ol.classList.add('toc-single-col');
        const links = [];
        const liElements = ol.querySelectorAll('li');
        liElements.forEach(li => {
          const a = li.querySelector('a');
          if (a) {
            links.push({
              href: a.getAttribute('href'),
              text: a.textContent.trim()
            });
          }
        });
        ol.innerHTML = '';
        links.forEach(link => {
          const li = document.createElement('li');
          const a = document.createElement('a');
          a.href = link.href;
          a.textContent = link.text;
          li.appendChild(a);
          ol.appendChild(li);
        });
      }
    }
  }
  
  // ===== 创建悬浮导航 =====
  const floatNav = document.createElement('div');
  floatNav.className = 'float-nav';
  
  // 获取上一篇/下一篇链接
  const topNav = document.querySelector('.doc-nav.top');
  let prevLink = '', nextLink = '';
  if (topNav) {
    const links = topNav.querySelectorAll('a');
    if (links.length >= 1 && !links[0].classList.contains('hidden')) {
      prevLink = links[0].href;
    }
    if (links.length >= 3) {
      nextLink = links[2].href;
    }
  }
  
  floatNav.innerHTML = `
    ${prevLink ? `<a href="${prevLink}" title="上一篇">←</a>` : ''}
    <a href="../index.html" class="home" title="返回首页">⌂</a>
    ${nextLink ? `<a href="${nextLink}" title="下一篇">→</a>` : ''}
    <a href="#" onclick="window.scrollTo({top:0,behavior:'smooth'});return false;" title="回到顶部">↑</a>
  `;
  
  document.body.appendChild(floatNav);
  
  // 滚动控制显示
  let lastScroll = 0;
  window.addEventListener('scroll', function() {
    const currentScroll = window.pageYOffset;
    
    // 滚动超过300px显示，向上滚动也显示
    if (currentScroll > 300) {
      floatNav.classList.add('show');
    } else {
      floatNav.classList.remove('show');
    }
    
    lastScroll = currentScroll;
  });
});
