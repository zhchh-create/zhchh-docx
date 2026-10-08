# -*- coding: utf-8 -*-
import io, re, os

ROOT = r"C:\Users\Administrator\Doubao\chats\2026-10-06\new-chat-1\技术栈详解"

def sec5_real(h3blocks):
    return ('<section id="sec5" class="card">\n'
      '  <h2><span class="num">5</span>实战项目经验（真实项目落地）</h2>\n'
      + h3blocks)

# each entry: (relpath, toc_text, body_html)
R = {}

# ---------- 01 Java基础【标准】 DCP-RMP Java17 ----------
R["07_后端开发/01_Java基础【标准】.html"] = ("实战项目经验（真实项目落地）", """
  <h3>1 项目背景</h3>
  <p class="lead"><b>一句话定位</b>：DCP-RMP（需求管理平台）后端是 SpringBoot 3 + Java 17 的单体服务，Java 语法特性贯穿日常每个接口的编写。</p>
  <ul>
    <li><strong>业务量级</strong>：需求/团队/工作流/AI 集成多模块，服务端日均处理数百次需求流转与评审操作（估算）。</li>
    <li><strong>为什么是 Java 17</strong>：团队 2026 年新项目直接选 LTS，用 record、switch 模式匹配、var、Stream 简化样板代码。</li>
  </ul>
  <h3>2 我的角色与职责</h3>
  <ul>
    <li><strong>分工</strong>：后端主力之一，负责需求域接口、通用查询、参数校验与异常处理，与 1 名前端对接联调（团队约 3-4 人，估算）。</li>
    <li><strong>范围</strong>：从 Controller 入参 DTO 到 Service 业务逻辑到 Mapper 出参全链路。</li>
  </ul>
  <h3>3 技术栈</h3>
  <ul><li><strong>组合</strong>：Java 17 + SpringBoot 3 + MyBatis + Redis(Redisson) + MySQL；构建 Maven/Gradle。</li></ul>
  <h3>4 落地设计</h3>
  <ul>
    <li><strong>不可变 DTO</strong>：入参出参用 <code>record</code> 替代手写 getter/setter，减少样板。</li>
    <li><strong>集合处理</strong>：把需求按状态分组、按处理人聚合，用 Stream 替代多层 for 循环。</li>
    <li><strong>异常分层</strong>：业务异常 <code>BizException</code> 抛出，全局处理器统一转错误结构，不把栈信息抛给前端。</li>
  </ul>
  <h3>5 关键实现要点</h3>
<pre class="code" data-lang="java"><code>// 出参不可变记录
public record ReqVO(Long id, String title, String status, String assigneeName) {}

// 按状态分组聚合，替代多层 for
Map&lt;String, List&lt;ReqVO&gt;&gt; byStatus = list.stream()
    .collect(Collectors.groupingBy(ReqVO::status));

// 业务异常 → 全局处理
if (req == null) throw new BizException("需求不存在", 40004);</code></pre>
  <h3>6 真实问题与解法</h3>
  <ul>
    <li><span class="tag-pit">坑</span><strong>自动拆箱 NPE</strong>：<code>Integer</code> 状态值为 null 时直接 <code>==</code> 比较拆箱 NPE——改 <code>Objects.equals(a,b)</code>。</li>
    <li><span class="tag-pit">坑</span><strong>equals 写反</strong>：用可能为 null 的变量调 <code>.equals()</code> 空指针——常量或枚举放前面。</li>
    <li><span class="tag-point">要点</span><strong>Stream 别滥用</strong>：简单循环里硬套 Stream 反而难读，只在分组/映射/过滤时用。</li>
  </ul>
  <h3>7 量化成果</h3>
  <ul><li>用 record + Stream 后，单个需求列表接口的 DTO 转换代码行数下降约一半（估算），可读性提升。</li></ul>
  <h3>8 协作与排期过程</h3>
  <ul><li>接口出入参随 OpenAPI 文档与前端对齐字段名，DTO 一改就同步文档，避免前后端字段名不一致返工。</li></ul>
  <h3>9 复盘与可复用经验</h3>
  <ul>
    <li><strong>空安全优先</strong>：所有外部入参先判空，业务异常集中抛。</li>
    <li><strong>不可变优先</strong>：DTO 用 record，减少可变状态。</li>
  </ul>
  <h3>10 面试讲法</h3>
  <p class="key-sentence">"DCP-RMP 后端用 Java 17，我用 record 简化 DTO、Stream 做分组聚合，并把异常统一到全局处理器，踩过自动拆箱 NPE 后养成了空安全习惯。"</p>
""")

# ---------- 02 Java并发与JVM【标准】 大屏分布式数据聚合 ----------
R["07_后端开发/02_Java并发与JVM【标准】.html"] = ("实战项目经验（真实项目落地）", """
  <h3>1 项目背景</h3>
  <p class="lead"><b>一句话定位</b>：电力大屏项目群（iClean 智能监控，Java + 前端）需要后端在短时间内聚合多个采集源的数据，供大屏高频刷新。</p>
  <ul>
    <li><strong>业务量级</strong>：一屏要汇总多个监控点位/设备的实时指标，后端要并行拉取再合并（估算并发：数十路采集源）。</li>
    <li><strong>痛点</strong>：串行逐个查采集源，一屏数据要等所有源依次返回，刷新延迟高。</li>
  </ul>
  <h3>2 我的角色与职责</h3>
  <ul>
    <li><strong>分工</strong>：负责大屏数据聚合后端接口，设计并行拉取与结果合并；前端由他人开发大屏图表。</li>
  </ul>
  <h3>3 技术栈</h3>
  <ul><li><strong>组合</strong>：Java + 线程池 + 并发容器；JVM 部署在应用服务器，用 G1/默认垃圾回收。</li></ul>
  <h3>4 落地设计</h3>
  <ul>
    <li><strong>并行拉取</strong>：用固定大小线程池并发调用各采集源，<code>CountDownLatch</code> 或 <code>CompletableFuture</code> 等齐后合并。</li>
    <li><strong>结果收集</strong>：多线程写结果用线程安全容器，避免 HashMap 并发丢数据。</li>
  </ul>
  <h3>5 关键实现要点</h3>
<pre class="code" data-lang="java"><code>ExecutorService pool = Executors.newFixedThreadPool(8);
List&lt;CompletableFuture&lt;Metric&gt;&gt; fs = sources.stream()
    .map(s -&gt; CompletableFuture.supplyAsync(() -&gt; fetch(s), pool))
    .toList();
Map&lt;String, Metric&gt; merged = fs.stream()
    .map(CompletableFuture::join)
    .collect(Collectors.toConcurrentMap(Metric::getSource, m -&gt; m));
// 任一采集源超时不能拖垮整屏：给 supplyAsync 加超时兜底</code></pre>
  <h3>6 真实问题与解法</h3>
  <ul>
    <li><span class="tag-pit">坑</span><strong>线程池无界 OOM</strong>：用 <code>newCachedThreadPool</code> 在高峰期线程暴涨——改用有界队列 + 拒绝策略。</li>
    <li><span class="tag-pit">坑</span><strong>一个采集源卡住拖垮整屏</strong>：并行拉取没设超时，某个源慢导致整屏等待——给每个 future 加超时降级（取不到用上次缓存）。</li>
    <li><span class="tag-point">要点</span><strong>JVM Full GC 卡顿</strong>：大屏接口高峰期偶发停顿，调大堆、用 G1 降低单次停顿。</li>
  </ul>
  <h3>7 量化成果</h3>
  <ul><li>聚合接口从串行的约 3 秒降到并行的约 800ms（估算，随采集源数量变化），大屏高频刷新不再明显卡顿。</li></ul>
  <h3>8 协作与排期过程</h3>
  <ul><li>与前端约定"超时降级返回上一帧缓存"，避免大屏空白闪烁；联调时固定一个模拟慢采集源压测。</li></ul>
  <h3>9 复盘与可复用经验</h3>
  <ul>
    <li><strong>并行必配超时</strong>：任何外部调用并行化都要带超时与降级。</li>
    <li><strong>线程池要定型</strong>：核心/最大线程、队列、拒绝策略显式配，不依赖默认。</li>
  </ul>
  <h3>10 面试讲法</h3>
  <p class="key-sentence">"大屏多源聚合我用线程池 + CompletableFuture 并行拉取并加超时降级，接口从约 3 秒降到约 800ms；踩过无界线程池和单源超时拖垮整屏的坑。"</p>
""")

# ---------- 03 Spring核心 IOC/AOP【深入】 DCP-RMP/源启 ----------
R["07_后端开发/03_Spring核心_IOC与AOP【深入】.html"] = ("实战项目经验（真实项目落地）", """
  <h3>1 项目背景</h3>
  <p class="lead"><b>一句话定位</b>：DCP-RMP 与源启后端都是 Spring 容器托管的分层应用，IOC 组装 Bean、AOP 横切日志/鉴权/事务。</p>
  <ul>
    <li><strong>业务量级</strong>：需求流转、团队权限、工作流节点，涉及多处"进接口先鉴权、写操作加事务、关键操作记日志"。</li>
  </ul>
  <h3>2 我的角色与职责</h3>
  <ul>
    <li><strong>分工</strong>：负责分层架构落地（Controller/Service/Mapper），编写鉴权切面、日志切面与事务边界。</li>
  </ul>
  <h3>3 技术栈</h3>
  <ul><li><strong>组合</strong>：SpringBoot 3 + Java 17 + MyBatis + Redis；AOP 用 Spring 自带代理。</li></ul>
  <h3>4 落地设计</h3>
  <ul>
    <li><strong>构造器注入</strong>：Service 依赖用构造器注入，字段注入 <code>@Autowired</code> 仅在测试临时用，保证可测试与不可变。</li>
    <li><strong>切面横切</strong>：登录态校验、操作日志、事务分别抽成切面/注解，业务代码不写样板。</li>
  </ul>
  <h3>5 关键实现要点</h3>
<pre class="code" data-lang="java"><code>@Service
@RequiredArgsConstructor                       // 构造器注入，依赖不可变
public class ReqService {
    private final ReqMapper reqMapper;
    private final ReqAssembler assembler;

    @Transactional(rollbackFor = Exception.class)   // 状态流转加事务
    public void review(Long id, ReviewCmd cmd) {
        Req r = reqMapper.selectById(id);
        r.apply(cmd);
        reqMapper.updateById(r);
    }
}

// 操作日志切面：对 @OpLog 注解的方法记录入参与结果
@Around("@annotation(opLog)")
public Object around(ProceedingJoinPoint pjp, OpLog opLog) throws Throwable { ... }</code></pre>
  <h3>6 真实问题与解法</h3>
  <ul>
    <li><span class="tag-pit">坑</span><strong>@Transactional 自调用失效</strong>：同类内 <code>this.otherMethod()</code> 调带注解方法，代理不生效、事务没开——把调用拆到另一个 Bean 或注入自己。</li>
    <li><span class="tag-pit">坑</span><strong>默认只回滚 RuntimeException</strong>：受检异常不回滚——显式 <code>rollbackFor = Exception.class</code>。</li>
    <li><span class="tag-pit">坑</span><strong>JDK 动态代理只代理接口</strong>：CGLIB 代理的类不能是 final；两者选择影响切面能否织入。</li>
  </ul>
  <h3>7 量化成果</h3>
  <ul><li>鉴权/日志/事务横切抽成切面后，业务 Service 方法不再夹带样板，单个方法平均少写 5-8 行重复代码（估算）。</li></ul>
  <h3>8 协作与排期过程</h3>
  <ul><li>切面统一在后端模块内维护，前端/接口定义不变；事务边界与 DBA 在评审"状态流转"用例时确认。</li></ul>
  <h3>9 复盘与可复用经验</h3>
  <ul>
    <li><strong>横切一律切面化</strong>：日志/鉴权/事务不进业务方法。</li>
    <li><strong>事务边界要清醒</strong>：自调用、异常类型是最高频失效点。</li>
  </ul>
  <h3>10 面试讲法</h3>
  <p class="key-sentence">"DCP-RMP 用构造器注入做分层，把鉴权/日志/事务抽成切面；我踩过 @Transactional 自调用失效和默认不回滚受检异常的坑，靠 rollbackFor 与拆 Bean 解决。"</p>
""")

# ---------- 04 SpringBoot【标准】 DCP-RMP/源启 ----------
R["07_后端开发/04_SpringBoot框架【标准】.html"] = ("实战项目经验（真实项目落地）", """
  <h3>1 项目背景</h3>
  <p class="lead"><b>一句话定位</b>：DCP-RMP 与源启后端都基于 SpringBoot 3 + Java 17，靠自动配置与 Starter 快速起服务。</p>
  <ul>
    <li><strong>业务量级</strong>：从一个 main 方法起服务，连上 MySQL、Redis，对外提供 REST 接口。</li>
  </ul>
  <h3>2 我的角色与职责</h3>
  <ul>
    <li><strong>分工</strong>：负责服务搭建、配置管理、接入 MyBatis/Redis 与接口暴露。</li>
  </ul>
  <h3>3 技术栈</h3>
  <ul><li><strong>组合</strong>：SpringBoot 3 + Web Starter + MyBatis Starter + Redis(Redisson) Starter；多环境配置 application-{dev,prod}.yml。</li></ul>
  <h3>4 落地设计</h3>
  <ul>
    <li><strong>约定优于配置</strong>：靠 starter 自动装配数据源/Redis/JSON，少写样板 XML。</li>
    <li><strong>配置外置</strong>：数据库地址、密钥走环境变量/多环境 profile，不硬编码。</li>
  </ul>
  <h3>5 关键实现要点</h3>
<pre class="code" data-lang="yaml"><code>spring:
  datasource:
    url: jdbc:mysql://${DB_HOST}/dcp_rmp
    username: ${DB_USER}
  data:
    redis:
      host: ${REDIS_HOST}
mybatis:
  mapper-locations: classpath:mapper/*.xml
  configuration:
    map-underscore-to-camel-case: true</code></pre>
<pre class="code" data-lang="java"><code>@SpringBootApplication
@MapperScan("com.dcp.rmp.mapper")
public class RmpApplication {
    public static void main(String[] args) {
        SpringApplication.run(RmpApplication.class, args);
    }
}</code></pre>
  <h3>6 真实问题与解法</h3>
  <ul>
    <li><span class="tag-pit">坑</span><strong>配置不生效</strong>：写错 profile 或 key，自动配置用了默认值——开 <code>--debug</code> 看 condition 报告。</li>
    <li><span class="tag-pit">坑</span><strong>Starter 版本冲突</strong>：手动引旧版依赖与 Boot 3 BOM 冲突——统一靠 parent BOM 管版本。</li>
    <li><span class="tag-point">要点</span><strong>Boot 3 包名变更</strong>：<code>javax.*</code> → <code>jakarta.*</code>，老依赖不兼容要换适配版。</li>
  </ul>
  <h3>7 量化成果</h3>
  <ul><li>新模块从建工程到跑通"数据库→接口"约半天（估算），自动配置省去手写数据源/事务管理器样板。</li></ul>
  <h3>8 协作与排期过程</h3>
  <ul><li>公共配置（数据源/Redis）由后端统一维护，各业务模块只加自己的业务配置；上线时由运维注入环境变量。</li></ul>
  <h3>9 复盘与可复用经验</h3>
  <ul>
    <li><strong>版本交给 BOM</strong>：不自管依赖版本。</li>
    <li><strong>敏感配置外置</strong>：密钥从不进 git。</li>
  </ul>
  <h3>10 面试讲法</h3>
  <p class="key-sentence">"两个后端都是 SpringBoot 3，我靠 starter 自动装配 + 多环境 profile 搭服务，踩过 javax→jakarta 迁移和配置不生效的坑，学会用 condition 报告排查自动配置。"</p>
""")

print("part A entries:", len(R))

APPLY = True
if APPLY:
    for rel, (toc, body) in R.items():
        fp = os.path.join(ROOT, rel.replace("/", os.sep))
        html = io.open(fp, encoding="utf-8").read()
        # TOC
        html, n1 = re.subn(r'<li><a href="#sec5">[^<]*</a></li>',
                           '<li><a href="#sec5">%s</a></li>' % toc, html, count=1)
        # sec5 block: from <section id="sec5" to just before <section id="sec6"
        new_block = '<section id="sec5" class="card">\n  <h2><span class="num">5</span>%s</h2>\n%s\n' % (toc, body)
        html, n2 = re.subn(r'<section id="sec5".*?(?=<section id="sec6")',
                           new_block, html, count=1, flags=re.S)
        io.open(fp, "w", encoding="utf-8", newline="\n").write(html)
        print(("OK " if n1 == 1 and n2 == 1 else "CHECK ") + rel, "toc=%d sec5=%d" % (n1, n2))
