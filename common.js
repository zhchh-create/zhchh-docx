// 悬浮导航显示/隐藏 + 修复目录树
document.addEventListener('DOMContentLoaded', function() {
  // ===== 修复左侧目录树 =====
  const toc = document.querySelector('nav.toc, .toc');
  if (toc) {
    toc.classList.add('sidebar-toc');
    
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
