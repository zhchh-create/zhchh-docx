/* ============================================================
 * 全栈技术栈详解 · 术语库
 * 每个术语：en 英文名 / cat 分类 / short 一句话定位 / detail 详细解释（可含 HTML）
 * 匹配规则：正文按 key 出现位置自动加下划线标注；点击弹窗看 detail。
 * ============================================================ */
window.GLOSSARY = window.GLOSSARY || {};

/* ---------- 01 前端基础 / JavaScript ---------- */
Object.assign(window.GLOSSARY, {
  "闭包": {
    en: "Closure",
    cat: "JavaScript",
    short: "函数把出生时所在的词法环境绑在自己身上，即使外层函数已返回仍能访问其中变量。",
    detail: "内部函数在创建时会捕获外层词法环境的引用；外部函数返回后，这个环境因仍被内部函数引用而不会被垃圾回收。<br><br><b>典型用途</b>：数据私有化（模块模式）、回调保持状态、函数柯里化、防抖节流。<br><br><b>典型坑</b>：被闭包长期引用的大对象不会被回收——长驻页面里用闭包持有大数组，会造成切屏后内存只涨不降。"
  },
  "词法作用域": {
    en: "Lexical Scope / Static Scope",
    cat: "JavaScript",
    short: "变量可见性由函数在源码中的书写位置决定，与谁调用它无关。",
    detail: "也叫静态作用域。函数在定义时就确定了它能访问哪些变量，而不是在调用时才决定。这是闭包成立的前提——正因为作用域由书写位置决定，内部函数才能捕获外层环境。"
  },
  "作用域链": {
    en: "Scope Chain",
    cat: "JavaScript",
    short: "沿父词法环境引用一路向上直到全局对象形成的链；查变量时从当前作用域开始沿链找，命中即停。",
    detail: "每进入一段可执行代码，引擎就建一个执行上下文，里面存当前作用域的变量声明与对外层词法环境的引用。变量查找时，从当前作用域开始，沿这条链逐级向上，直到命中或到达全局对象（未命中就是 undefined）。"
  },
  "执行上下文": {
    en: "Execution Context",
    cat: "JavaScript",
    short: "引擎为每段可执行代码创建的运行环境——全局一个、每次函数调用一个。",
    detail: "执行上下文记录当前作用域的变量环境、this 绑定、以及对外层词法环境的引用。调用栈压入/弹出的就是一个个执行上下文。栈顶上下文决定当前可见的变量与 this。"
  },
  "调用栈": {
    en: "Call Stack",
    cat: "JavaScript",
    short: "记录\"现在执行到哪个函数、该返回哪里\"的栈结构。",
    detail: "JS 是单线程执行：同一时刻只跑一段代码。每进入一个函数就压入一个执行上下文，函数返回就弹出。栈有上限（V8 约一万余帧），递归过深就是栈溢出（Stack Overflow）。"
  },
  "动态类型": {
    en: "Dynamic Typing",
    cat: "JavaScript",
    short: "变量不绑定类型，值才有类型；类型检查发生在运行期而非编译期。",
    detail: "同一个变量今天存数字、明天存字符串都合法。工程上的代价是把错误推迟到运行期——所以要靠 TypeScript、显式转换、严格相等（===）把不确定性前移。"
  },
  "隐式转换": {
    en: "Implicit Coercion",
    cat: "JavaScript",
    short: "运算符两侧类型不一致时引擎自动转换类型，是大量\"看起来对其实错\"的根因。",
    detail: "例如 <code>+</code> 遇字符串会拼接，<code>==</code> 按抽象相等规则辗转比较。<br><br><b>工程铁律</b>：比较一律用 <code>===</code>（不转换、值与类型都比）；需要转换时显式写 <code>Number(x)</code> / <code>String(x)</code>，不依赖引擎的隐式行为。"
  },
  "原始类型": {
    en: "Primitive Type",
    cat: "JavaScript",
    short: "number / string / boolean / null / undefined / symbol / bigint 七种，赋值拷贝值。",
    detail: "原始类型按值传递——赋值时拷贝的是值本身，修改新变量不影响旧变量。与之相对的是 object（含数组、函数），赋值只拷贝引用，两边指向同一个对象。"
  },
  "this 绑定": {
    en: "this Binding",
    cat: "JavaScript",
    short: "this 不看函数定义在哪，而看它\"怎么被调用\"——四条规则按优先级裁决。",
    detail: "<b>优先级从高到低：</b><br>1. <b>new 调用</b>：<code>new Foo()</code>，this 是新创建的实例。<br>2. <b>显式绑定</b>：<code>foo.call/apply/bind(ctx)</code>，this 是手动传入的 ctx。<br>3. <b>隐式绑定</b>：<code>obj.foo()</code>，this 是调用点前面的对象 obj。<br>4. <b>默认绑定</b>：直接 <code>foo()</code>，严格模式是 undefined，非严格是全局对象。<br><br><b>箭头函数</b>不绑定自己的 this，捕获定义处的 this——回调里\"this 丢了\"的标准解法。"
  },
  "原型链": {
    en: "Prototype Chain",
    cat: "JavaScript",
    short: "JS 没有经典继承，对象靠内部指针 [[Prototype]] 把属性查找沿链向上委托。",
    detail: "每个对象内部有隐藏指针 <code>__proto__</code> 指向另一个对象；自身没有的属性沿链向上找，直到 <code>null</code>。<br><br><b>prototype vs __proto__</b>：<code>prototype</code> 是函数的属性，指向\"实例的原型对象\"；<code>__proto__</code> 是实例指向其原型对象的链接。两者方向相反，最易混淆。<br><br><b>设计动机</b>：所有实例共享同一份方法（挂在 prototype 上），节省内存。"
  },
  "原型污染": {
    en: "Prototype Pollution",
    cat: "JavaScript",
    short: "随意给 Object.prototype 或原型对象塞方法，导致全局对象被污染的安全问题。",
    detail: "<code>for...in</code> 会把原型上可枚举的属性也遍历出来，必须用 <code>hasOwnProperty</code> 过滤。恶意输入可通过 <code>__proto__</code> 注入污染方法，被第三方库利用——前端安全常见考点。"
  },
  "垃圾回收": {
    en: "Garbage Collection, GC",
    cat: "JavaScript",
    short: "V8 靠\"可达性\"决定回收：从根出发能到达的对象保留，不可达的回收。",
    detail: "早期引用计数因循环引用被淘汰；现代引擎以<b>标记-清除</b>为主，辅以分代回收（新生代 Scavenge、老生代 Mark-Compact）。<br><br><b>前端内存泄漏三类典型</b>：未解绑的事件监听、忘记清理的定时器、被闭包或全局数组长期持有的大对象。"
  },
  "WeakMap": {
    en: "WeakMap / WeakSet",
    cat: "JavaScript",
    short: "key 是弱引用，不阻止 GC 回收——给 DOM/对象挂附加数据的标准做法。",
    detail: "<code>weakMap.set(el, meta)</code>：元素被销毁后条目自动消失，避免\"全局表长期持有大对象\"导致内存泄漏。<br><br>与 Map 的区别：WeakMap 的 key 必须是对象，且不可枚举（无法遍历）。"
  },
  "暂时性死区": {
    en: "Temporal Dead Zone, TDZ",
    cat: "JavaScript",
    short: "let/const 在声明前访问会抛 ReferenceError 的区域。",
    detail: "<code>let/const</code> 是块级作用域，存在提升但不让访问——从块开始到声明语句之间就是 TDZ。这与 <code>var</code>（提升后值为 undefined，可访问）形成对比。"
  },
  "模块模式": {
    en: "Module Pattern",
    cat: "JavaScript",
    short: "用闭包实现私有变量与公开接口的经典设计模式。",
    detail: "通过立即执行函数（IIFE）返回对象，内部变量被闭包保护，外部只能经暴露的方法访问——ES Modules 普及前实现模块化的标准做法。"
  },
  "函数柯里化": {
    en: "Currying",
    cat: "JavaScript",
    short: "把多参数函数拆成一连串单参数函数的转换技巧。",
    detail: "<code>add(1)(2)(3)</code> 这种形式。每次调用返回一个新函数接住下一个参数，靠闭包留住之前的参数。常用于参数预置、函数式组合。"
  },
  "防抖": {
    en: "Debounce",
    cat: "JavaScript",
    short: "事件停止触发 N 毫秒后才执行一次，常用于输入搜索、窗口 resize。",
    detail: "高频触发的事件（如 input、scroll）只在\"停下来\"后执行一次。实现核心就是闭包保存 timer 句柄，每次触发清掉旧 timer 重设新 timer。"
  },
  "节流": {
    en: "Throttle",
    cat: "JavaScript",
    short: "高频事件在 N 毫秒内只执行一次，保证固定频率，常用于滚动、mousemove。",
    detail: "与防抖的区别：节流是\"固定频率执行\"，防抖是\"停下来才执行\"。滚动加载、拖拽跟动用节流；搜索联想、窗口 resize 用防抖。"
  },
  "事件委托": {
    en: "Event Delegation",
    cat: "JavaScript",
    short: "利用事件冒泡，把子元素的监听绑在父元素上，统一处理。",
    detail: "动态添加的子元素无需重新绑定监听；同时减少监听器数量。jQuery 时代 <code>$(parent).on('click', '.child', fn)</code> 是标准写法。"
  },
  "CommonJS": {
    en: "CommonJS, CJS",
    cat: "JavaScript",
    short: "Node.js 早期模块规范，运行时动态加载，值拷贝。",
    detail: "<code>require / module.exports</code>。对原始类型导出的是值快照（首次 require 时拷贝），对对象仍是共享引用。<br><br><b>坑</b>：改了导出对象的字段页面没更新，往往就是值拷贝/活绑定的差异所致。"
  },
  "ESM": {
    en: "ES Modules",
    cat: "JavaScript",
    short: "ES2015 标准化的模块规范，编译期静态分析，支持 tree-shaking。",
    detail: "<code>import / export</code>。绑定是活的（导出值变，导入方跟着变）；模块只执行一次、形成单例。新代码一律 ESM，老 CommonJS 靠工具兼容。"
  },
  "tree-shaking": {
    en: "Tree Shaking",
    cat: "工程化",
    short: "构建时移除未被引用的导出代码，减小产物体积。",
    detail: "依赖 ESM 的静态结构——只有编译期能确定 import/export 关系，才能做死代码消除。CommonJS 因为是运行时动态加载，无法 tree-shake。Vite/Webpack 生产构建默认开启。"
  },
  "IIFE": {
    en: "Immediately Invoked Function Expression",
    cat: "JavaScript",
    short: "定义即立即执行的函数表达式，用来创建独立作用域。",
    detail: "<code>(function(){ ... })()</code>。ES6 块级作用域普及前，用来避免变量污染全局——经典闭包陷阱（for 循环 var）的修复手段就是用 IIFE 立即传参。"
  },

  /* ---------- 通用工程术语（跨篇复用） ---------- */
  "BFC": {
    en: "Block Formatting Context",
    cat: "CSS",
    short: "块级格式化上下文，决定盒子如何布局以及与其他元素的相互作用。",
    detail: "触发条件：float、position:absolute、display:inline-block/flex/grid、overflow:hidden 等。<br><br><b>常见作用</b>：清除浮动、防止 margin 重叠、阻止元素被浮动元素覆盖。"
  },
  "响应式": {
    en: "Responsive Design",
    cat: "CSS",
    short: "同一套代码适配不同屏幕尺寸的设计思路。",
    detail: "核心三要素：弹性布局（Flex/Grid）、相对单位（rem/%/vw/vh）、媒体查询。大屏项目群用 rem 适配 + 媒体查询做多分辨率。"
  },
  "XSS": {
    en: "Cross-Site Scripting",
    cat: "安全",
    short: "攻击者注入恶意脚本到网页，在受害者浏览器执行。",
    detail: "三类：存储型（恶意脚本存服务器）、反射型（URL 参数带脚本）、DOM 型（前端渲染时拼接）。<br><br><b>防御</b>：输入校验、输出转义、CSP、HttpOnly Cookie。富文本场景需白名单清洗（DOMPurify）。"
  },
  "CSRF": {
    en: "Cross-Site Request Forgery",
    cat: "安全",
    short: "诱导用户在已登录状态下发起非本意的请求。",
    detail: "与 XSS 的区别：XSS 是偷用户身份，CSRF 是冒充用户发请求。<br><br><b>防御</b>：CSRF Token、SameSite Cookie、验证 Referer/Origin、敏感操作二次确认。"
  },
  "CORS": {
    en: "Cross-Origin Resource Sharing",
    cat: "Web",
    short: "浏览器跨源资源共享机制，后端通过响应头授权跨域请求。",
    detail: "浏览器同源策略（协议+域名+端口任一不同即跨域）拦住跨源请求；后端设置 <code>Access-Control-Allow-Origin</code> 等响应头来放行。预检请求（OPTIONS）用于复杂请求。"
  },
  "虚拟 DOM": {
    en: "Virtual DOM",
    cat: "框架",
    short: "用 JS 对象描述真实 DOM，状态变更时先在虚拟树 diff，再批量更新真实 DOM。",
    detail: "React/Vue 的核心抽象。代价是多一层 JS 计算，收益是跨平台渲染（Native/Canvas）和声明式编程。Vue3 引入编译期优化后，虚拟 DOM 的运行时开销进一步降低。"
  },
  "SSR": {
    en: "Server-Side Rendering",
    cat: "框架",
    short: "服务端把组件渲染成 HTML 字符串再发给浏览器。",
    detail: "收益：首屏快、SEO 友好。代价：服务器压力大、开发受限（不能用 window/document）。Nuxt/Next.js 是主流方案。与 SSG（静态生成）、SPA（纯客户端渲染）对比选型。"
  },
  "微前端": {
    en: "Micro Frontends",
    cat: "架构",
    short: "把大型前端应用拆成多个独立部署的小子应用，运行时集成。",
    detail: "典型方案：qiankun（基于 single-spa）、Module Federation。核心问题：JS 沙箱（隔离全局变量）、样式隔离（Shadow DOM/CSS Module）、公共依赖共享、路由分发。"
  },
  "WebRTC": {
    en: "Web Real-Time Communication",
    cat: "实时通信",
    short: "浏览器间点对点实时音视频与数据通道的标准。",
    detail: "核心三件套：<b>PeerConnection</b>（连接管理）、<b>SDP</b>（会话描述协议，协商编解码）、<b>ICE/STUN/TURN</b>（NAT 穿透）。需要信令服务器交换 SDP/ICE 候选，但媒体流不走服务器（P2P）。"
  },
  "SFU": {
    en: "Selective Forwarding Unit",
    cat: "实时通信",
    short: "媒体网关：只转发不混流，每个订阅者收到自己需要的流。",
    detail: "与 MCU（混流器）的区别：SFU 转发多路独立流，客户端解码压力大但服务器成本低；MCU 在服务器端混流成一路，客户端简单但服务器重。Janus、mediasoup 都是 SFU 架构。"
  },
  "JWT": {
    en: "JSON Web Token",
    cat: "后端",
    short: "无状态的跨域鉴权令牌，Header.Payload.Signature 三段 Base64 拼接。",
    detail: "服务端签发后客户端存储（localStorage/Cookie），每次请求带在 Authorization 头。服务端验签即可，不存 session。<br><br><b>注意</b>：JWT 本身不加密，敏感信息不要放 payload；注销需配合黑名单或短有效期 + Refresh Token。"
  },
  "MVCC": {
    en: "Multi-Version Concurrency Control",
    cat: "数据库",
    short: "多版本并发控制：读不阻塞写、写不阻塞读，靠 undo log 快照实现。",
    detail: "InnoDB 实现。每行数据有多个版本，读操作根据隔离级别读对应版本的快照，写操作生成新版本。是 MySQL 事务隔离级别（RC/RR）的底层实现。"
  },
  "B+ 树": {
    en: "B+ Tree",
    cat: "数据库",
    short: "MySQL InnoDB 默认索引结构，多路平衡查找树，叶子节点存数据、链表相连。",
    detail: "与 B 树的区别：非叶子节点不存数据只存索引，叶子节点双向链表相连——范围查询快、磁盘 IO 少。主键索引（聚簇索引）叶子节点存整行数据；二级索引叶子节点存主键值（回表）。"
  },
  "缓存穿透": {
    en: "Cache Penetration",
    cat: "Redis",
    short: "查询不存在的数据，缓存不命中，请求全部打到数据库。",
    detail: "<b>防御</b>：① 缓存空值（短 TTL）；② 布隆过滤器（在缓存前挡一层，判断 key 一定不存在就直接返回）。"
  },
  "缓存击穿": {
    en: "Cache Breakdown",
    cat: "Redis",
    short: "某个热点 key 过期瞬间，大量并发请求同时打到数据库。",
    detail: "<b>防御</b>：① 互斥锁（只放一个请求去查库重建缓存）；② 热点 key 永不过期，后台异步更新。"
  },
  "缓存雪崩": {
    en: "Cache Avalanche",
    cat: "Redis",
    short: "大量 key 同时过期，或 Redis 宕机，请求全部涌向数据库。",
    detail: "<b>防御</b>：① 过期时间加随机偏移，避免同时失效；② 缓存高可用（哨兵/集群）；③ 限流降级兜底。"
  },
  "Redisson": {
    en: "Redisson",
    cat: "Redis",
    short: "Redis 官方推荐的 Java 客户端，提供分布式锁、分布式集合等高级工具。",
    detail: "<b>看门狗机制</b>：加锁默认 30s，后台线程每 10s 续期，避免业务未执行完锁就过期。<br><br><b>注意</b>：可重入锁、公平锁、红锁（RedLock）的取舍；主从切换时锁丢失问题。"
  },
  "IoC": {
    en: "Inversion of Control",
    cat: "Spring",
    short: "控制反转：对象的创建与依赖注入交给容器，而非自己 new。",
    detail: "Spring 核心思想。Bean 由 IoC 容器管理生命周期，依赖关系在配置/注解中声明。DI（依赖注入）是 IoC 的实现方式——构造器注入、Setter 注入、字段注入。"
  },
  "AOP": {
    en: "Aspect-Oriented Programming",
    cat: "Spring",
    short: "面向切面编程：把日志、事务、权限等横切逻辑从业务代码中抽离。",
    detail: "底层是动态代理（JDK 代理接口 / CGLIB 代理类）。<code>@Transactional</code> 就是最典型的 AOP 应用——方法前后自动开启/提交/回滚事务。"
  },
  "Nacos": {
    en: "Nacos",
    cat: "微服务",
    short: "阿里开源的服务注册发现 + 配置中心。",
    detail: "替代 Eureka + Spring Cloud Config。服务启动时注册自己，消费方从 Nacos 拉取服务列表并做负载均衡；配置变更实时推送（长轮询）。"
  },
  "Kafka": {
    en: "Apache Kafka",
    cat: "消息队列",
    short: "高吞吐分布式发布订阅消息系统，基于磁盘顺序写 + 零拷贝。",
    detail: "模型：Topic → Partition → Consumer Group。顺序写磁盘 + PageCache 实现百万级 TPS。<br><br><b>适用</b>：日志采集、大数据管道、事件溯源。<b>不适用</b>：需要严格延迟和事务的场景（用 RabbitMQ/RocketMQ）。"
  },
  "Docker": {
    en: "Docker",
    cat: "DevOps",
    short: "容器化引擎：把应用和依赖打包成镜像，在任意环境一致运行。",
    detail: "<b>镜像分层</b>：每个 Dockerfile 指令一层，可缓存复用。<br><b>容器 vs 虚拟机</b>：容器共享宿主内核，启动毫秒级；VM 跑完整 Guest OS，启动分钟级。<br><b>Compose</b>：单机多容器编排。"
  },
  "Kubernetes": {
    en: "K8s",
    cat: "DevOps",
    short: "容器编排系统：自动部署、扩缩容、故障恢复服务发现。",
    detail: "核心对象：<b>Pod</b>（最小调度单位，包一个或多个容器）、<b>Deployment</b>（管理 Pod 副本与滚动更新）、<b>Service</b>（稳定访问入口，负载均衡）、<b>探针</b>（liveness/readiness 健康检查）。"
  },
  "Nginx": {
    en: "Nginx",
    cat: "DevOps",
    short: "高性能 HTTP 服务器与反向代理，事件驱动异步非阻塞模型。",
    detail: "三大用途：① 静态资源托管；② 反向代理（转发到后端 Tomcat/Node）；③ 负载均衡（轮询/加权/ip_hash）。<br><br>配合 gzip、缓存头、HTTPS 终止。"
  },
  "RAG": {
    en: "Retrieval-Augmented Generation",
    cat: "AI",
    short: "检索增强生成：先从知识库检索相关文档，再让大模型基于文档回答。",
    detail: "解决大模型知识过时、幻觉、私有数据无法训练的问题。流程：文档切片 → 向量化 → 存入向量库 → 用户提问时检索 Top-K 相关片段 → 拼入 Prompt → LLM 生成答案。"
  },
  "Function Calling": {
    en: "Function Calling / Tool Use",
    cat: "AI",
    short: "大模型根据用户意图决定调用哪个外部函数，并生成参数。",
    detail: "LLM 本身不执行函数，只输出\"该调哪个函数、参数是什么\"的结构化 JSON；由应用层真正执行函数，再把结果喂回 LLM 生成最终回答。是 AI Agent 的基础能力。"
  },

  /* ---------- CSS / HTML / 浏览器 ---------- */
  "盒模型": {
    en: "Box Model",
    cat: "CSS",
    short: "内容(content) + 内边距(padding) + 边框(border) + 外边距(margin) 四层结构。",
    detail: "<code>box-sizing: content-box</code>（默认，width 只算内容）vs <code>border-box</code>（width 含 padding+border）。工程上全局 <code>* { box-sizing: border-box }</code> 避免宽度计算混乱。"
  },
  "层叠上下文": {
    en: "Stacking Context",
    cat: "CSS",
    short: "决定元素 Z 轴叠放顺序的独立层叠环境。",
    detail: "触发条件：根元素、position+z-index、opacity<1、transform、filter、flex 子项等。<br><br><b>易混点</b>：z-index 只在同一层叠上下文内比较；父子层叠上下文隔离，子元素 z-index 再高也跑不出父层。"
  },
  "重排": {
    en: "Reflow / Layout",
    cat: "浏览器",
    short: "几何属性变化触发浏览器重新计算元素位置和大小。",
    detail: "也叫回流。改 width/height/top/left、字体、窗口大小都会触发。<b>优化</b>：批量改样式（class 切换）、脱离文档流（position:absolute/fixed）、用 transform 替代 top/left。"
  },
  "重绘": {
    en: "Repaint",
    cat: "浏览器",
    short: "外观变化但几何位置不变，浏览器只重新绘制颜色/背景。",
    detail: "改 color/background/visibility 只触发重绘，比重排便宜。<br><br>渲染管线：重排 → 重绘 → 合成。用 transform/opacity 走合成器线程，不触发重排重绘。"
  },
  "事件循环": {
    en: "Event Loop",
    cat: "JavaScript",
    short: "JS 单线程下协调调用栈、宏任务队列、微任务队列的执行机制。",
    detail: "执行栈清空后，先清空所有微任务（Promise.then/queueMicrotask/MutationObserver），再取一个宏任务（setTimeout/setInterval/I/O/UI 事件），执行完再清微任务，循环往复。<br><br><b>面试必考</b>：async/await 是 Promise 语法糖，await 后面的代码相当于 .then。"
  },
  "宏任务": {
    en: "Macro Task",
    cat: "JavaScript",
    short: "每次 Event Loop 迭代执行一个的任务，如 setTimeout、setInterval、I/O、UI 事件。",
    detail: "与微任务相对。宏任务进入 Event Table，达到时机后回调进入宏任务队列，每次循环取一个执行。"
  },
  "微任务": {
    en: "Micro Task",
    cat: "JavaScript",
    short: "当前宏任务执行完后立即清空的任务，如 Promise.then、queueMicrotask。",
    detail: "微任务优先级高于下一个宏任务。所有微任务在 UI 渲染前清空。这也是为什么 Promise 比 setTimeout 先执行。"
  },
  "Promise": {
    en: "Promise",
    cat: "JavaScript",
    short: "异步操作的容器，三种状态：pending → fulfilled / rejected。",
    detail: "解决回调地狱。链式调用 .then/.catch/.finally。<code>Promise.all/race/allSettled/all</code> 是组合多个异步的工具。"
  },
  "async": {
    en: "async / await",
    cat: "JavaScript",
    short: "Promise 的语法糖，让异步代码写起来像同步。",
    detail: "<code>await</code> 会暂停函数执行，等待 Promise resolve。await 后面的代码相当于 .then 回调，属于微任务。<br><br><b>坑</b>：for 循环里多个 await 是串行的，要并行用 Promise.all。"
  },
  "渲染管线": {
    en: "Rendering Pipeline",
    cat: "浏览器",
    short: "从 HTML/CSS 到屏幕像素的流水线：DOM/CSSOM → 渲染树 → 布局 → 绘制 → 合成。",
    detail: "1. <b>DOM/CSSOM</b>：解析 HTML/CSS 成两棵树；2. <b>渲染树</b>：只含可见节点；3. <b>布局(Layout)</b>：算几何；4. <b>绘制(Paint)</b>：填像素；5. <b>合成(Composite)</b>：图层合并上屏。<br><br>改 transform/opacity 只触发合成，最快。"
  },
  "V8": {
    en: "V8 Engine",
    cat: "浏览器",
    short: "Chrome/Node.js 的 JS 引擎，负责解析、JIT 编译、GC。",
    detail: "内联缓存(IC)、隐藏类(Hidden Class)、惰性解析、基线编译+优化编译(Backend)。JS 性能优化本质是帮助 V8 做类型稳定。"
  },
  "WebGL": {
    en: "WebGL",
    cat: "可视化",
    short: "浏览器里的 GPU 硬件加速绘图 API，基于 OpenGL ES。",
    detail: "通过 GLSL 着色器语言直接操作 GPU。Three.js 是它的上层封装。万级数据点渲染靠 WebGL 而非 Canvas 2D——后者是 CPU 绘制，会卡。"
  },
  "Canvas": {
    en: "Canvas 2D",
    cat: "可视化",
    short: "CPU 绘制位图的 2D 绘图 API，适合小数据量、复杂像素操作。",
    detail: "与 SVG 的区别：Canvas 是位图（缩放模糊、靠 JS 重绘），SVG 是矢量 DOM（支持事件、缩放不失真）。千级以上元素用 Canvas/WebGL。"
  },

  /* ---------- TypeScript ---------- */
  "泛型": {
    en: "Generics",
    cat: "TypeScript",
    short: "类型层面的参数化——把类型当作参数传递，提升复用性。",
    detail: "<code>function identity<T>(x: T): T</code>。常见约束 <code>extends</code>、默认类型 <code>=</code>、多泛型 <code>&lt;T, K&gt;</code>。是 React/Vue 组件 props 类型的基础。"
  },
  "联合类型": {
    en: "Union Type",
    cat: "TypeScript",
    short: "值可以是多种类型之一，用 <code>|</code> 连接。",
    detail: "<code>type Status = 'open' | 'closed' | 'pending'</code>。比 string 更安全——只能取字面量之一，写错编辑器直接报错。"
  },
  "类型推导": {
    en: "Type Inference",
    cat: "TypeScript",
    short: "TS 自动根据值推断类型，不必处处显式标注。",
    detail: "<code>const n = 1</code> 推导为 <code>number</code>。函数返回值也能推导。<b>原则</b>：边界（函数参数/返回值）显式标注，内部靠推导。"
  },

  /* ---------- Vue / 框架 ---------- */
  "响应式": {
    en: "Reactivity",
    cat: "Vue",
    short: "数据变化自动触发视图更新——Vue 的核心机制。",
    detail: "Vue2 用 <code>Object.defineProperty</code> 劫持 getter/setter；Vue3 用 <code>Proxy</code> 代理整个对象，解决数组下标/新增属性检测不到的问题。<br><br>effect 副作用函数在数据变更时被调度器批量执行。"
  },
  "Proxy": {
    en: "Proxy",
    cat: "Vue",
    short: "ES6 元编程特性，拦截对象的全套操作，Vue3 响应式基础。",
    detail: "可拦截 get/set/has/deleteProperty 等 13 种操作。相比 Object.defineProperty 能监听数组下标、属性新增删除，且惰性递归（访问到才代理子对象）。"
  },
  "虚拟 DOM diff": {
    en: "Virtual DOM Diff",
    cat: "框架",
    short: "新旧虚拟树对比，找出最小变更批量更新真实 DOM。",
    detail: "同层比较、key 复用列表节点。Vue3 编译期优化：静态提升、PatchFlag（只动态绑定的部分打标记）、Block Tree（跳过静态子树）。"
  },
  "插槽": {
    en: "Slot",
    cat: "Vue",
    short: "组件内容分发机制——父组件往子组件指定位置塞模板。",
    detail: "<code>&lt;slot&gt;</code> 是占位符；具名插槽 <code>v-slot:name</code>、作用域插槽 <code>&lt;slot :data=\"x\"&gt;</code> 把子组件数据回传给父组件。"
  },
  "Hooks": {
    en: "Hooks",
    cat: "React",
    short: "React 函数组件里复用状态逻辑的机制（useState/useEffect 等）。",
    detail: "<b>规则</b>：只在顶层调用、只在 React 函数里调用。依赖数组决定 effect 何时重跑。自定义 Hooks（useXxx）是逻辑复用的主要方式。"
  },

  /* ---------- 工程化 ---------- */
  "loader": {
    en: "Webpack Loader",
    cat: "工程化",
    short: "Webpack 的文件转换器，把非 JS 文件转成 Webpack 能处理的模块。",
    detail: "链式执行，从右到左、从下到上。<code>css-loader/style-loader/babel-loader/vue-loader</code>。每个文件类型配对应 loader。"
  },
  "plugin": {
    en: "Webpack Plugin",
    cat: "工程化",
    short: "Webpack 的事件钩子扩展，参与整个构建流程。",
    detail: "通过 tapable 挂钩到编译生命周期。常见：HtmlWebpackPlugin（生成 HTML）、CleanWebpackPlugin、DefinePlugin、压缩插件。与 loader 的区别：loader 管文件转换，plugin 管构建事件。"
  },
  "HMR": {
    en: "Hot Module Replacement",
    cat: "工程化",
    short: "模块热替换——改代码后不刷新整页，只替换变更模块。",
    detail: "Webpack dev server 核心能力。保留应用状态，开发体验好。Vite 基于原生 ESM 实现，更快。"
  },
  "虚拟列表": {
    en: "Virtual List",
    cat: "性能",
    short: "长列表只渲染可视区域内的 DOM，滚动时动态替换。",
    detail: "千行以上列表的性能关键。原理：容器固定高度，计算可视区间 start/end，只渲染这部分，用 padding 撑开占位。vxe-table、react-window 都是这个思路。"
  },
  "懒加载": {
    en: "Lazy Loading",
    cat: "性能",
    short: "路由/图片/组件在需要时才加载，减小首屏体积。",
    detail: "路由级：<code>() =&gt; import('./Xxx.vue')</code> 代码分包；图片级：<code>loading=\"lazy\"</code> 或 IntersectionObserver。"
  },
  "Monorepo": {
    en: "Monorepo",
    cat: "工程化",
    short: "多个 package/子项目放在一个 Git 仓库统一管理。",
    detail: "工具：pnpm workspace、Turborepo（任务编排+增量缓存）、Nx。<b>收益</b>：跨包重构原子化、统一版本/规范。<b>代价</b>：仓库变大、CI 变慢（靠增量缓存解决）。"
  },

  /* ---------- 后端 / Java / Spring ---------- */
  "JVM": {
    en: "Java Virtual Machine",
    cat: "后端",
    short: "Java 字节码运行环境，包含类加载、内存模型、GC。",
    detail: "内存分区：堆(对象)、栈(栈帧/局部变量)、方法区(类元信息)、PC 寄存器、本地方法栈。调优主要调堆大小(-Xms/-Xmx)和 GC 算法。"
  },
  "线程池": {
    en: "Thread Pool",
    cat: "后端",
    short: "预先创建若干线程复用，避免频繁创建销毁。",
    detail: "核心参数：corePoolSize、maxPoolSize、queue、keepAliveTime、拒绝策略。Spring 默认 Tomcat 线程池 200。<br><br><b>生产禁忌</b>：不要用 Executors.newCachedThreadPool（无界队列 OOM），手动 new ThreadPoolExecutor。"
  },
  "Bean 生命周期": {
    en: "Bean Lifecycle",
    cat: "Spring",
    short: "Bean 从实例化到销毁的完整流程，Spring 在各环节留扩展点。",
    detail: "实例化 → 属性填充 → Aware 接口回调 → BeanPostProcessor.before → @PostConstruct → InitializingBean → 使用 → @PreDestroy → DisposableBean。<br><br>AOP 代理正是在 BeanPostProcessor 环节包出来的。"
  },
  "动态代理": {
    en: "Dynamic Proxy",
    cat: "Spring",
    short: "运行时生成代理类，在方法前后插入横切逻辑。",
    detail: "JDK 代理（基于接口）、CGLIB 代理（继承目标类，不能代理 final）。Spring AOP 默认：有接口用 JDK，无接口用 CGLIB。<code>@Transactional/@Async</code> 都是代理实现。"
  },
  "MyBatis": {
    en: "MyBatis",
    cat: "后端",
    short: "半自动化 ORM：SQL 自己写，参数映射和结果集封装交给框架。",
    detail: "核心对象：SqlSession（会话）、Executor（执行器）、Mapper 代理接口。<br><br><b>关键</b>：<code>#{}</code> 预编译防注入，<code>${}</code> 字符串拼接有注入风险；一级缓存 SqlSession 级，二级缓存 Mapper 级。"
  },
  "ORM": {
    en: "Object-Relational Mapping",
    cat: "后端",
    short: "对象关系映射——把数据库表映射成 Java 对象。",
    detail: "MyBatis 是半自动（SQL 手写），JPA/Hibernate 是全自动（方法名生成 SQL）。MyBatis-Plus 在 MyBatis 上加 CRUD 自动生成。"
  },
  "RESTful": {
    en: "RESTful API",
    cat: "后端",
    short: "用 HTTP 方法表达操作、URL 表达资源的 API 设计风格。",
    detail: "GET 查、POST 增、PUT 改、DELETE 删。状态码：200/201/400/401/403/404/500。版本号放 URL 头或 Header。"
  },
  "OAuth2": {
    en: "OAuth 2.0",
    cat: "后端",
    short: "开放授权协议——让第三方应用在用户授权下访问其资源。",
    detail: "四种授权模式：授权码（最常用）、隐式、密码、客户端凭证。SSO（单点登录）基于它。与 JWT 配合：OAuth2 签发 token，JWT 是 token 的一种格式。"
  },
  "RabbitMQ": {
    en: "RabbitMQ",
    cat: "消息队列",
    short: "基于 AMQP 协议的传统消息队列，路由灵活、低延迟。",
    detail: "模型：Producer → Exchange（交换机）→ Binding → Queue → Consumer。四种交换机：direct/topic/fanout/headers。<br><br><b>适用</b>：业务通知、订单、延迟队列。高吞吐不如 Kafka。"
  },

  /* ---------- 数据库 ---------- */
  "聚簇索引": {
    en: "Clustered Index",
    cat: "数据库",
    short: "叶子节点存整行数据的索引，InnoDB 主键即聚簇索引。",
    detail: "一张表只能有一个聚簇索引（数据按主键顺序组织）。二级索引叶子节点存主键值，查二级索引后需要<b>回表</b>再到聚簇索引取整行。"
  },
  "最左前缀": {
    en: "Leftmost Prefix",
    cat: "数据库",
    short: "联合索引 (a,b,c) 只能从最左列开始匹配，不能跳过。",
    detail: "索引 (name, age, city) 能命中 name、(name,age)、(name,age,city)，但不能直接用 age/city。<br><br>范围查询（&gt;、&lt;、like）后面的列索引失效。"
  },
  "回表": {
    en: "Bookmark Lookup",
    cat: "数据库",
    short: "二级索引查到主键后，再到聚簇索引取整行数据的过程。",
    detail: "<b>覆盖索引</b>解决：查询列都在索引里就不用回表。例如索引 (name, age)，查 <code>select name,age where name=?</code> 直接从索引返回。"
  },
  "事务隔离级别": {
    en: "Transaction Isolation Level",
    cat: "数据库",
    short: "定义事务间可见性的标准，从低到高：读未提交/读已提交/可重复读/串行化。",
    detail: "解决三类问题：脏读、不可重复读、幻读。<br><br>MySQL InnoDB 默认<b>可重复读(RR)</b>，靠 MVCC + 间隙锁基本解决幻读。Oracle 默认读已提交(RC)。"
  },
  "主从复制": {
    en: "Master-Slave Replication",
    cat: "数据库",
    short: "主库写、从库读，通过 binlog 同步数据。",
    detail: "三种复制格式：statement(逻辑 SQL)、row(行变更)、mixed。<br><br>读写分离：写走主库、读走从库，从库延迟是常见坑。"
  },
  "分库分表": {
    en: "Sharding",
    cat: "数据库",
    short: "数据量过大时按规则拆分到多个库/表。",
    detail: "垂直拆分（按业务拆库）、水平拆分（按用户 ID/时间 hash 取模拆表）。<b>代价</b>：跨库 JOIN、分布式事务、全局 ID、扩容数据迁移。中间件：ShardingSphere。"
  },
  "倒排索引": {
    en: "Inverted Index",
    cat: "数据库",
    short: "ES/Lucene 的索引结构：词 → 文档列表，支持全文检索。",
    detail: "与正向索引（文档 → 词）相反。分词后每个词项记录出现在哪些文档的哪些位置。是 Elasticsearch/Lucene 全文检索的基础。"
  },

  /* ---------- Redis ---------- */
  "Redis 持久化": {
    en: "RDB / AOF",
    cat: "Redis",
    short: "RDB 是快照（某时刻全量），AOF 是追加写命令日志。",
    detail: "RDB：体积小、恢复快，但可能丢最后一次快照后的数据。<br>AOF：每条写命令追加，更安全但文件大、恢复慢。生产常用 AOF everysec（最多丢 1 秒）。"
  },
  "过期策略": {
    en: "Redis Eviction",
    cat: "Redis",
    short: "Redis key 过期删除 + 内存满时的淘汰策略。",
    detail: "<b>过期删除</b>：惰性（访问时检查）+ 定期（随机抽样删）。<br><b>内存淘汰</b>：noeviction(默认)、allkeys-lru(最常用)、volatile-lru、allkeys-lfu 等。"
  },

  /* ---------- DevOps ---------- */
  "反向代理": {
    en: "Reverse Proxy",
    cat: "DevOps",
    short: "代理服务器接收请求，转发给后端，客户端不知道真实后端。",
    detail: "与正向代理（代理客户端访问外网）相对。Nginx 是最常见的反向代理。收益：负载均衡、SSL 终止、缓存、安全隔离。"
  },
  "负载均衡": {
    en: "Load Balancer",
    cat: "DevOps",
    short: "把请求分发到多个后端实例，分摊压力。",
    detail: "算法：轮询、加权轮询、ip_hash（会话粘滞）、least_conn。层：四层（TCP/IP，LVS）、七层（HTTP，Nginx/Ingress）。"
  },
  "CI/CD": {
    en: "Continuous Integration / Deployment",
    cat: "DevOps",
    short: "持续集成 + 持续部署：代码提交后自动构建、测试、部署。",
    detail: "Pipeline 阶段：checkout → install → lint → test → build → docker build → push → deploy。Jenkins/GitLab CI/GitHub Actions 是工具。"
  },
  "探针": {
    en: "Probe",
    cat: "K8s",
    short: "K8s 容器健康检查：liveness（死了重启）、readiness（没就绪不接流量）、startup（启动宽限）。",
    detail: "没配 readiness 探针会导致滚动更新时旧实例已停、新实例未就绪，流量打空。"
  },

  /* ---------- 实时通信 ---------- */
  "WebSocket": {
    en: "WebSocket",
    cat: "实时通信",
    short: "全双工通信协议，HTTP 握手后升级为 ws:// 长连接。",
    detail: "与轮询/SSE 的区别：WebSocket 双向、低延迟、服务器可主动推。<br><br>工程要点：心跳包保活、断线重连、消息序列号去重。"
  },
  "SDP": {
    en: "Session Description Protocol",
    cat: "实时通信",
    short: "WebRTC 会话描述协议：描述编解码、IP、端口等媒体能力。",
    detail: "通过信令服务器交换 offer/answer SDP，双方对齐媒体能力。SDP 本身不走媒体，只协商元信息。"
  },
  "ICE": {
    en: "Interactive Connectivity Establishment",
    cat: "实时通信",
    short: "WebRTC 连接建立框架：收集候选地址、探测可达性。",
    detail: "流程：收集 host(本机)/srflx(公网映射，STUN)/relay(TURN 中转) 候选 → 按优先级连通性检查。<br><br>STUN 打洞失败时走 TURN 服务器转发。"
  },

  /* ---------- Git ---------- */
  "rebase": {
    en: "Git Rebase",
    cat: "工程化",
    short: "把提交搬到另一个基底上，保持线性历史。",
    detail: "与 merge 的区别：merge 生成合并提交、历史分叉；rebase 重放提交、历史干净。<br><br><b>铁律</b>：不要 rebase 已经推到公共分支的提交。"
  },
  "merge conflict": {
    en: "Merge Conflict",
    cat: "工程化",
    short: "Git 合并时同一文件同一处被不同分支修改产生的冲突。",
    detail: "手动编辑文件保留正确代码，<code>git add</code> 后 <code>git rebase --continue</code> / <code>git commit</code> 完成合并。"
  }
});
