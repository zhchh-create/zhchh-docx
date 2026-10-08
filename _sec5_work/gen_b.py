# -*- coding: utf-8 -*-
import io, re, os
ROOT = r"C:\Users\Administrator\Doubao\chats\2026-10-06\new-chat-1\技术栈详解"
R = {}

REAL = "实战项目经验（真实项目落地）"
DEMO = "实战项目经验（自学 + 自建 Demo）"

# 05 SSH框架【基础】 demo 型
R["07_后端开发/05_SSH框架【基础】.html"] = (DEMO, """
  <div class="warn-box"><b>定位说明：</b>SSH（Struts2 + Spring + Hibernate）是 Java Web 早期经典组合，本人简历项目已演进到 SpringBoot + MyBatis，未在近年项目使用 SSH。本节为最小骨架复刻与演进理解笔记，非企业项目履历。</div>
  <h3>1 自学背景与动机</h3>
  <p class="lead"><b>一句话定位</b>：补"现代 SpringBoot 之前 Java Web 长什么样"的历史认知，理解框架为何从 SSH 演进到注解 + 自动配置。</p>
  <ul><li><strong>缺口</strong>：直接上手 SpringBoot，不清楚 XML 重配置、Struts2 拦截器栈、Hibernate ORM 映射的来龙去脉。</li></ul>
  <h3>2 搭建的 demo 是什么</h3>
  <ul>
    <li><strong>技术栈</strong>：Struts2 + Spring + Hibernate 三框架整合的最小 Web 工程，一个登录 + 列表查询。</li>
    <li><strong>规模</strong>：单体 war 包跑在 Tomcat，一张用户表，走"Action→Service→DAO(Hibernate)"。</li>
  </ul>
  <h3>3 落地步骤</h3>
<pre class="code" data-lang="xml"><code>&lt;!-- Spring 托管 Bean，Hibernate SessionFactory 由 Spring 管理 --&gt;
&lt;bean id="sessionFactory"
      class="org.springframework.orm.hibernate5.LocalSessionFactoryBean"&gt;
  &lt;property name="dataSource" ref="dataSource"/&gt;
&lt;/bean&gt;</code></pre>
<pre class="code" data-lang="xml"><code>&lt;!-- Struts2 把请求映射到 Spring 容器里的 Action --&gt;
&lt;action name="login" class="loginAction" method="execute"&gt;
  &lt;result name="success"&gt;/list.jsp&lt;/result&gt;
&lt;/action&gt;</code></pre>
  <h3>4 自学过程中遇到的坑与解决</h3>
  <ul>
    <li><span class="tag-pit">坑</span><strong>配置量大</strong>：数据源、SessionFactory、事务、Action 全在 XML，改一处翻半天——这正是 SpringBoot 自动配置要消灭的痛点。</li>
    <li><span class="tag-pit">坑</span><strong>Struts2 版本安全漏洞</strong>：早期版本有远程命令执行历史，复现时刻意用归档版本仅本地学习。</li>
  </ul>
  <h3>5 成果</h3>
  <ul><li>跑通后能讲清"请求→Struts2 拦截器→Spring 托管的 Action→Hibernate 操作数据库"整条链路，并对比出 SpringBoot 删掉了哪些配置。</li></ul>
  <h3>6 与真实项目的差异</h3>
  <ul><li>这是理解性 demo，未上生产；近年项目用 SpringBoot + MyBatis，SSH 仅作演进脉络参考。</li></ul>
  <h3>7 面试讲法</h3>
  <p class="key-sentence">"我用最小工程复刻过 Struts2+Spring+Hibernate，理解了 XML 重配置和 ORM 映射的代价，这也是我快速接受 SpringBoot 自动配置的原因。"</p>
""")

# 06 MyBatis持久层【深入】 real (merge existing two cases into 10 subblocks)
R["07_后端开发/06_MyBatis持久层【深入】.html"] = (REAL, """
  <h3>1 项目背景</h3>
  <p class="lead"><b>一句话定位</b>：源启（SpringBoot3+MyBatis+Redis）与 DCP-RMP 的持久层都用 MyBatis，承担动态 SQL、分页、批量与复杂结果映射。</p>
  <ul><li><strong>业务量级</strong>：配置项组合查询、需求列表 join 出团队/处理人，多为列表型读多写少（估算）。</li></ul>
  <h3>2 我的角色与职责</h3>
  <ul><li><strong>分工</strong>：负责 Mapper 接口与 XML 编写、分页接入、复杂结果映射，与前端约定列表查询条件。</li></ul>
  <h3>3 技术栈</h3>
  <ul><li><strong>组合</strong>：SpringBoot 3 + MyBatis + PageHelper 分页插件 + MySQL。</li></ul>
  <h3>4 落地设计</h3>
  <ul>
    <li><strong>动态 SQL</strong>：列表查询用 <code>&lt;where&gt;+&lt;if&gt;</code>，前端传哪个条件拼哪个，一个接口覆盖组合筛选。</li>
    <li><strong>批量写</strong>：节点配置批量保存改 <code>&lt;foreach&gt;</code> 多 values，按 500 条分批。</li>
    <li><strong>避免 N+1</strong>：需求列表 join 出团队名/处理人名，resultMap 映射嵌套 DTO。</li>
  </ul>
  <h3>5 关键实现要点</h3>
<pre class="code" data-lang="java"><code>public PageInfo&lt;ConfigItem&gt; query(ConfigQuery q) {
    PageHelper.startPage(q.getPage(), q.getSize());   // 紧跟下一条查询
    List&lt;ConfigItem&gt; list = configMapper.search(q);
    return new PageInfo&lt;&gt;(list);
}</code></pre>
<pre class="code" data-lang="xml"><code>&lt;resultMap id="reqVoMap" type="RequirementVO"&gt;
  &lt;id property="id" column="id"/&gt;
  &lt;result property="teamName" column="team_name"/&gt;
  &lt;result property="assigneeName" column="assignee_name"/&gt;
&lt;/resultMap&gt;
&lt;select id="listVo" resultMap="reqVoMap"&gt;
  SELECT r.*, t.team_name, u.user_name AS assignee_name
  FROM t_requirement r
  LEFT JOIN t_team t ON r.team_id = t.id
  LEFT JOIN t_user u ON r.assignee = u.id
  WHERE r.status = #{status}
&lt;/select&gt;</code></pre>
  <h3>6 真实问题与解法</h3>
  <ul>
    <li><span class="tag-pit">坑</span><strong>PageHelper 作用错语句</strong>：startPage 后紧跟了无关 count 查询——它是 ThreadLocal，必须紧贴目标查询。</li>
    <li><span class="tag-pit">坑</span><strong>N+1</strong>：早期对每条需求再查团队，列表 100 行发 101 条 SQL、打开等两秒；改 join 后一条搞定（约 2s→<300ms，估算）。</li>
    <li><span class="tag-pit">坑</span><strong>join 后 id 列映射串了</strong>：两表都有 id，<code>&lt;id column="id"&gt;</code> 混淆——给列起别名。</li>
    <li><span class="tag-pit">坑</span><strong>单字符 status 的 OGNL</strong>：字符串条件要写 <code>status != null and status != ''</code>。</li>
  </ul>
  <h3>7 量化成果</h3>
  <ul><li>批量保存从循环逐条数秒降到几百毫秒；需求列表从 101 条 SQL 降到 1 条，打开明显变快（均为估算）。</li></ul>
  <h3>8 协作与排期过程</h3>
  <ul><li>列表筛选条件随前端需求迭代，动态 SQL 让后端不必为每个新条件加接口；分页参数与前端表格组件约定 page/size。</li></ul>
  <h3>9 复盘与可复用经验</h3>
  <ul>
    <li><strong>列表先想 join</strong>：展示字段能一次 join 出来就不要 N+1。</li>
    <li><strong>批量必分批</strong>：foreach 一次别太大，按几百条一批。</li>
  </ul>
  <h3>10 面试讲法</h3>
  <p class="key-sentence">"源启和 DCP-RMP 都用 MyBatis，我用动态 SQL 做组合查询、foreach 做批量、join+resultMap 消除 N+1；踩过 PageHelper 贴错语句和 N+1 各发 101 条 SQL 的坑。"</p>
""")

# 07 Tomcat与Jetty【基础】 real
R["07_后端开发/07_Tomcat与Jetty服务器【基础】.html"] = (REAL, """
  <h3>1 项目背景</h3>
  <p class="lead"><b>一句话定位</b>：DCP-RMP/源启 SpringBoot 服务默认内嵌 Tomcat，打包成 jar 直接运行，部署在应用服务器上。</p>
  <ul><li><strong>业务量级</strong>：内部管理系统，并发量不高但要稳定常驻，偶尔有多人同时操作。</li></ul>
  <h3>2 我的角色与职责</h3>
  <ul><li><strong>分工</strong>：负责服务打包、JVM 与连接参数调整，配合运维把 jar 部署到服务器。</li></ul>
  <h3>3 技术栈</h3>
  <ul><li><strong>组合</strong>：SpringBoot 内嵌 Tomcat（Web 容器）+ jar 部署；外置 Tomcat 仅作了解。</li></ul>
  <h3>4 落地设计</h3>
  <ul>
    <li><strong>内嵌优于外置</strong>：SpringBoot 把 Tomcat 打进 jar，一条命令起服务，省去外部容器与 war 部署。</li>
    <li><strong>连接参数</strong>：按需调整 server.tomcat.threads.max 与连接超时，匹配内部系统并发。</li>
  </ul>
  <h3>5 关键实现要点</h3>
<pre class="code" data-lang="yaml"><code>server:
  port: 8080
  tomcat:
    threads:
      max: 200
      min-spare: 10
    accept-count: 100</code></pre>
  <h3>6 真实问题与解法</h3>
  <ul>
    <li><span class="tag-pit">坑</span><strong>端口占用起不来</strong>：上次进程没退干净——部署脚本先查端口再起。</li>
    <li><span class="tag-point">要点</span><strong>内嵌 vs 外置</strong>：新项目一律内嵌；多应用共用一个容器才考虑外置 Tomcat。</li>
  </ul>
  <h3>7 量化成果</h3>
  <ul><li>服务启动从"打 war→部署外部容器→重启"简化为一条 java -jar（约几分钟→一条命令）。</li></ul>
  <h3>8 协作与排期过程</h3>
  <ul><li>部署方式与运维约定：jar + 启动脚本，端口/线程数在配置里可调，不写死在代码。</li></ul>
  <h3>9 复盘与可复用经验</h3>
  <ul><li><strong>优先内嵌</strong>：SpringBoot 项目不折腾外置容器。</li><li><strong>连接参数按并发调</strong>：内部系统不必盲目开大线程。</li></ul>
  <h3>10 面试讲法</h3>
  <p class="key-sentence">"SpringBoot 服务用内嵌 Tomcat 打 jar 部署，我按内部系统并发调过线程数与 accept-count，理解了内嵌与外置容器的取舍。"</p>
""")

# 08 Swagger与OpenAPI【标准】 real —— 亮点案例
R["07_后端开发/08_Swagger与OpenAPI接口契约【标准】.html"] = (REAL, """
  <h3>1 项目背景</h3>
  <p class="lead"><b>一句话定位</b>：DCP-RMP 是前后端分离 + Monorepo（pnpm workspace），后端 SpringBoot 用 Swagger/OpenAPI 自动产出接口文档，并据此生成前端 TS 接口客户端。</p>
  <ul><li><strong>业务量级</strong>：需求/团队/工作流接口数十个，前后端分离下接口字段多、联调频繁（估算）。</li></ul>
  <h3>2 我的角色与职责</h3>
  <ul><li><strong>分工</strong>：后端写接口与注解、产出 OpenAPI 文档；牵头把文档接到前端自动生成 TS 客户端的流水线。</li></ul>
  <h3>3 技术栈</h3>
  <ul><li><strong>组合</strong>：SpringBoot 3 + springdoc-openapi（产出 OpenAPI 3 文档）→ 前端用 openapi 工具按文档生成 TS API 客户端。</li></ul>
  <h3>4 落地设计</h3>
  <ul>
    <li><strong>契约先行</strong>：后端定好接口路径/入参出参，导出 OpenAPI JSON。</li>
    <li><strong>代码生成</strong>：前端跑脚本把 OpenAPI 生成类型化 TS 客户端，调用时自动带类型。</li>
    <li><strong>单源真相</strong>：接口文档是后端注解生成的唯一来源，不再手维护一份易过期的 md。</li>
  </ul>
  <h3>5 关键实现要点</h3>
<pre class="code" data-lang="java"><code>@RestController
@RequestMapping("/api/requirements")
@Tag(name = "需求管理")
public class ReqController {
    @Operation(summary = "需求列表")
    @GetMapping
    public Result&lt;PageVO&lt;ReqVO&gt;&gt; list(ReqQuery q) { ... }
}</code></pre>
<pre class="code" data-lang="bash"><code># 后端启动后导出 OpenAPI，前端据此生成 TS 客户端
npx openapi-typescript http://localhost:8080/v3/api-docs -o src/api/schema.ts</code></pre>
  <h3>6 真实问题与解法</h3>
  <ul>
    <li><span class="tag-pit">坑</span><strong>返回 Result 包没在文档里说明</strong>：生成的 TS 类型拿不到外层 code/data 结构——补统一响应包装的 schema。</li>
    <li><span class="tag-pit">坑</span><strong>枚举字段生成成 string</strong>：后端枚举没标注，前端类型丢失——用 @Schema(allowableValues) 显式声明。</li>
    <li><span class="tag-point">要点</span><strong>文档要随版本提交</strong>：生成脚本进 npm script，接口一改重新生成，避免前后端类型漂移。</li>
  </ul>
  <h3>7 量化成果</h3>
  <ul><li>联调阶段"字段名对不上/类型不对"类沟通大幅减少（估算：原先约三成联调时间耗在接口字段对齐上）；前端调用直接拿到类型提示。</li></ul>
  <h3>8 协作与排期过程</h3>
  <ul><li>契约先行：后端先出接口与 OpenAPI，前端据此并行开发页面，不再等后端接口写完；联调时差异点直接看生成的类型。</li></ul>
  <h3>9 复盘与可复用经验</h3>
  <ul>
    <li><strong>接口文档即代码</strong>：注解生成 + 提交版本，杜绝过期文档。</li>
    <li><strong>响应包装要建模</strong>：统一 Result/PageVO 必须在 schema 里体现。</li>
  </ul>
  <h3>10 面试讲法</h3>
  <p class="key-sentence">"DCP-RMP 我把 OpenAPI 文档自动生成 TS 客户端接到 Monorepo 里，契约先行让前后端并行开发，联调字段对齐的沟通基本消失。"</p>
""")

# 09 RESTful_API设计【标准】 real
R["07_后端开发/09_RESTful_API设计【标准】.html"] = (REAL, """
  <h3>1 项目背景</h3>
  <p class="lead"><b>一句话定位</b>：DCP-RMP 与源启后端对外都走 REST 风格 HTTP 接口，资源命名、状态码、分页、错误结构需要统一约定。</p>
  <ul><li><strong>业务量级</strong>：需求/团队/配置等资源的增删改查，前端与大屏都在调。</li></ul>
  <h3>2 我的角色与职责</h3>
  <ul><li><strong>分工</strong>：参与制定接口规范，落地资源命名、统一响应包装与错误结构。</li></ul>
  <h3>3 技术栈</h3>
  <ul><li><strong>组合</strong>：SpringBoot REST + 统一 Result 包装 + OpenAPI 文档。</li></ul>
  <h3>4 落地设计</h3>
  <ul>
    <li><strong>资源用名词</strong>：<code>/api/requirements</code>，操作用 HTTP 动词，不用 <code>/listReq</code>。</li>
    <li><strong>统一响应</strong>：所有接口包 <code>{code, message, data}</code>，分页返回 <code>{list, total}</code>。</li>
    <li><strong>错误结构</strong>：业务错误返回约定 code + message，不抛栈。</li>
  </ul>
  <h3>5 关键实现要点</h3>
<pre class="code" data-lang="http"><code>GET    /api/requirements?page=1&amp;size=20&amp;status=REVIEW
POST   /api/requirements
GET    /api/requirements/123
PUT    /api/requirements/123
PATCH  /api/requirements/123/status     # 状态流转用 PATCH
DELETE /api/requirements/123</code></pre>
<pre class="code" data-lang="json"><code>{ "code": 0, "message": "ok",
  "data": { "list": [ ... ], "total": 138 } }</code></pre>
  <h3>6 真实问题与解法</h3>
  <ul>
    <li><span class="tag-pit">坑</span><strong>动作型接口硬凑 REST</strong>："审批通过"不是资源 CRUD——用 PATCH 子资源 <code>/status</code> 或受控动作路径，别发明 <code>/api/passReq</code>。</li>
    <li><span class="tag-pit">坑</span><strong>分页参数不统一</strong>：有的 pageNo/pageSize、有的 page/size——全局统一一套。</li>
  </ul>
  <h3>7 量化成果</h3>
  <ul><li>接口风格统一后，前端按约定即可猜出路径，新资源接口文档阅读成本下降（估算）。</li></ul>
  <h3>8 协作与排期过程</h3>
  <ul><li>与前端约定分页参数与错误码字典，配合 OpenAPI 生成客户端，风格不一致的接口在评审时纠正。</li></ul>
  <h3>9 复盘与可复用经验</h3>
  <ul><li><strong>名词 + 动词</strong>：资源名词，动作用 HTTP method。</li><li><strong>统一包装</strong>：分页与错误结构全项目一套。</li></ul>
  <h3>10 面试讲法</h3>
  <p class="key-sentence">"DCP-RMP 我落地 REST 规范：资源用名词、状态流转用 PATCH、统一 Result 与分页结构，和 OpenAPI 生成客户端配合，前后端对接口不再靠口头约定。"</p>
""")

# 10 接口安全 JWT【标准】 real
R["07_后端开发/10_接口安全_JWT与鉴权【标准】.html"] = (REAL, """
  <h3>1 项目背景</h3>
  <p class="lead"><b>一句话定位</b>：DCP-RMP 前后端分离，登录态用 JWT，接口经拦截器校验令牌，再按角色做 RBAC 权限。</p>
  <ul><li><strong>业务量级</strong>：多用户/多团队协作，登录后访问需求与评审接口。</li></ul>
  <h3>2 我的角色与职责</h3>
  <ul><li><strong>分工</strong>：实现登录签发 JWT、拦截器校验、登出/刷新与接口级权限控制。</li></ul>
  <h3>3 技术栈</h3>
  <ul><li><strong>组合</strong>：SpringBoot 拦截器 + JWT 库 + Redis（存刷新令牌/黑名单）+ RBAC 角色。</li></ul>
  <h3>4 落地设计</h3>
  <ul>
    <li><strong>签发</strong>：登录成功签发 access token（短时效），refresh token 存 Redis。</li>
    <li><strong>校验</strong>：拦截器从 Authorization 头取 token，验签 + 查黑名单，解析出 userId/role 放入上下文。</li>
    <li><strong>权限</strong>：接口按角色/资源判定能不能操作。</li>
  </ul>
  <h3>5 关键实现要点</h3>
<pre class="code" data-lang="java"><code>public boolean preHandle(HttpServletRequest req, HttpServletResponse resp, Object h) {
    String token = req.getHeader("Authorization");
    if (token == null || blacklist.exists(token)) throw new BizException("未登录", 401);
    Claims c = Jwts.parser().setSigningKey(secret).parseClaimsJws(token).getBody();
    UserContext.set(Long.valueOf(c.getSubject()), c.get("role", String.class));
    return true;   // 后续方法再做资源级权限校验
}</code></pre>
  <h3>6 真实问题与解法</h3>
  <ul>
    <li><span class="tag-pit">坑</span><strong>JWT 无法主动失效</strong>：登出后 token 在过期前仍可用——登出把 token 加入 Redis 黑名单，拦截器先查黑名单。</li>
    <li><span class="tag-pit">坑</span><strong>密钥硬编码</strong>：签名密钥写代码里泄漏——放配置/环境变量。</li>
    <li><span class="tag-point">要点</span><strong>access 要短时效</strong>：用短 access + 长 refresh 控制泄漏窗口。</li>
  </ul>
  <h3>7 量化成果</h3>
  <ul><li>无状态登录省去服务端 session 存储；登出/失效通过黑名单补齐（token 约 2h 过期，refresh 约 7 天，估算）。</li></ul>
  <h3>8 协作与排期过程</h3>
  <ul><li>与前端约定 Authorization 头格式与 401 跳登录；角色清单与产品/业务确认后落到权限表。</li></ul>
  <h3>9 复盘与可复用经验</h3>
  <ul><li><strong>无状态要补失效</strong>：JWT + Redis 黑名单是标准组合。</li><li><strong>密钥与时效</strong>：密钥外置、access 短时效。</li></ul>
  <h3>10 面试讲法</h3>
  <p class="key-sentence">"DCP-RMP 我用 JWT + 拦截器做登录态，access 短时效配 Redis 黑名单解决 JWT 登出失效问题，再叠 RBAC 做接口级权限。"</p>
""")

# 11 SpringCloud demo
R["07_后端开发/11_SpringCloud微服务与网关【标准】.html"] = (DEMO, """
  <div class="warn-box"><b>定位说明：</b>本人简历项目（DCP-RMP、源启）后端均为 SpringBoot 单体，未实际拆分微服务。本节为本地三服务自学 demo 与"单体向微服务演进"评估，非企业项目履历。</div>
  <h3>1 自学背景与动机</h3>
  <p class="lead"><b>一句话定位</b>：补"单体拆成微服务后注册发现、网关、声明式调用怎么串"的链路认知。</p>
  <ul><li><strong>缺口</strong>：一直写单体，不清楚 Nacos 注册、Gateway 路由、Feign 互调的真实链路。</li></ul>
  <h3>2 搭建的 demo 是什么</h3>
  <ul>
    <li><strong>结构</strong>：Nacos 注册中心 + 服务 A（提供者）+ 服务 B（消费者）+ Gateway 网关，跑通"注册→网关路由→Feign 互调"最小闭环。</li>
    <li><strong>规模</strong>：本地四个进程，SpringBoot 3 + 对应版本 SpringCloud Alibaba。</li>
  </ul>
  <h3>3 落地步骤</h3>
<pre class="code" data-lang="yaml"><code># Gateway 路由：按路径转发到注册中心里的服务
spring:
  cloud:
    gateway:
      routes:
        - id: service-a
          uri: lb://service-a        # lb 表示走注册中心负载均衡
          predicates: [ Path=/a/** ]</code></pre>
<pre class="code" data-lang="java"><code>@FeignClient("service-a")          // 按服务名调用，不写死地址
public interface AClient {
    @GetMapping("/a/hello") String hello();
}</code></pre>
  <h3>4 自学过程中遇到的坑与解决</h3>
  <ul>
    <li><span class="tag-pit">坑</span><strong>Boot 与 Cloud 版本不匹配</strong>：Boot3 配了 Boot2 时代 Cloud 版本，启动报类找不到——先查版本兼容矩阵再选。</li>
    <li><span class="tag-pit">坑</span><strong>Gateway 用阻塞 API</strong>：网关是 WebFlux 响应式，误写阻塞调用会报警告——保持链路非阻塞。</li>
  </ul>
  <h3>5 成果</h3>
  <ul><li>本地跑通注册→路由→Feign 互调，能用一句话讲清一次请求经过网关、注册中心、服务提供者的完整路径。</li></ul>
  <h3>6 与真实项目的差异</h3>
  <ul><li>单机 demo 无高可用、无配置中心灰度、无链路追踪；对 DCP-RMP 的评估结论是"现阶段单体 + 模块化即可，微服务是技术储备"。</li></ul>
  <h3>7 面试讲法</h3>
  <p class="key-sentence">"我用 Nacos+Gateway+Feign 本地搭过最小微服务闭环，理解注册发现与路由链路；同时能讲清为什么我评估 DCP-RMP 现阶段不该过早拆微服务。"</p>
""")

# 12 Kafka demo
R["07_后端开发/12_消息队列_Kafka与RabbitMQ【标准】.html"] = (DEMO, """
  <div class="warn-box"><b>定位说明：</b>本人简历项目未实际部署消息队列。本节为本地 Kafka 生产/消费自学 demo，用于验证 topic/分区/消费者组与削峰模型，非企业项目履历。</div>
  <h3>1 自学背景与动机</h3>
  <p class="lead"><b>一句话定位</b>：补"异步解耦、削峰填谷到底怎么落地"的认知，尤其大屏告警高峰可能需要的削峰场景。</p>
  <ul><li><strong>缺口</strong>：项目都是同步调用，不清楚消息队列的投递语义、分区与消费者组。</li></ul>
  <h3>2 搭建的 demo 是什么</h3>
  <ul>
    <li><strong>结构</strong>：本地 Kafka（单节点）+ 一个生产者 + 一个消费者组，写"告警事件"topic，多分区、多消费实例并行消费。</li>
    <li><strong>规模</strong>：脚本压一批消息模拟高峰写入，观察消费滞后与并发。</li>
  </ul>
  <h3>3 落地步骤</h3>
<pre class="code" data-lang="java"><code>// 生产者：告警事件异步投递，不阻塞主接口
kafkaTemplate.send("alarm-events", deviceId, eventJson);

// 消费者组：同组内分区被均衡分配给各实例
@KafkaListener(topics = "alarm-events", groupId = "alarm-handler")
public void onMessage(ConsumerRecord&lt;String,String&gt; rec) {
    handle(rec.value());
}</code></pre>
  <h3>4 自学过程中遇到的坑与解决</h3>
  <ul>
    <li><span class="tag-pit">坑</span><strong>重复消费</strong>：手动提交位移前业务异常，重投后重复处理——消费端做幂等（按事件 id 去重）。</li>
    <li><span class="tag-pit">坑</span><strong>分区数决定并行度</strong>：3 分区起 5 个消费实例也只有 3 个在消费——并行度上限=分区数。</li>
  </ul>
  <h3>5 成果</h3>
  <ul><li>跑通生产/消费，验证了"高峰写队列、后端按能力匀速消费"的削峰模型，并理解消费者组与分区的关系。</li></ul>
  <h3>6 与真实项目的差异</h3>
  <ul><li>单节点无副本、无监控；未上生产。对应大屏告警削峰/异步化是规划中的演进方向。</li></ul>
  <h3>7 面试讲法</h3>
  <p class="key-sentence">"我本地搭过 Kafka 生产消费 demo，亲手验证了分区数决定并行度、消费端要幂等；理解它如何给大屏告警高峰削峰，也清楚真实生产还要副本与监控。"</p>
""")

# 13 SpringSecurity real (DCP-RMP JWT + 演进对比)
R["07_后端开发/13_SpringSecurity与OAuth2【标准】.html"] = (REAL, """
  <h3>1 项目背景</h3>
  <p class="lead"><b>一句话定位</b>：DCP-RMP 实际用的是自研 JWT 拦截器做登录态与鉴权；本节讲真实落地，并对比 Spring Security 过滤器链这条演进路线。</p>
  <ul><li><strong>业务量级</strong>：多用户/团队协作，登录态校验 + RBAC 权限。</li></ul>
  <h3>2 我的角色与职责</h3>
  <ul><li><strong>分工</strong>：实现并维护现有 JWT 拦截器；同时调研若改用 Spring Security，过滤器链该怎么组织。</li></ul>
  <h3>3 技术栈</h3>
  <ul><li><strong>组合</strong>（现状）：SpringBoot 拦截器 + JWT + Redis 黑名单；<b>演进对比对象</b>：Spring Security 过滤器链 + OAuth2/SSO。</li></ul>
  <h3>4 落地设计</h3>
  <ul>
    <li><strong>现状（拦截器）</strong>：一个 HandlerInterceptor 统一验签、查黑名单、塞 UserContext，业务接口再判权限。</li>
    <li><strong>对比（过滤器链）</strong>：Spring Security 用一串 Filter 完成"认证→授权→异常处理"，职责拆分更细、生态更全。</li>
  </ul>
  <h3>5 关键实现要点</h3>
<pre class="code" data-lang="java"><code>// 现状：自研拦截器（DCP-RMP 真实做法）
public boolean preHandle(...) {
    String token = req.getHeader("Authorization");
    if (token == null || blacklist.exists(token)) throw new BizException("未登录", 401);
    UserContext.set(parseUser(token));
    return true;
}</code></pre>
<pre class="code" data-lang="java"><code>// 演进：Spring Security 过滤器链思路（对比学习，未上线）
http.authorizeHttpRequests(auth -&gt; auth
    .requestMatchers("/api/admin/**").hasRole("ADMIN")
    .anyRequest().authenticated())
   .addFilterBefore(jwtFilter, UsernamePasswordAuthenticationFilter.class);</code></pre>
  <h3>6 真实问题与解法</h3>
  <ul>
    <li><span class="tag-pit">坑</span><strong>拦截器漏放行静态/登录接口</strong>：拦截器配错把登录接口也拦了——白名单要明确。</li>
    <li><span class="tag-point">要点</span><strong>何时换 Spring Security</strong>：需要 OAuth2/SSO、细粒度方法级权限、多登录方式时，自研拦截器会越写越重，过滤器链更划算。</li>
  </ul>
  <h3>7 量化成果</h3>
  <ul><li>现有拦截器满足 DCP-RMP 当前"单系统 JWT + RBAC"需求，实现轻、易维护；评估结论：暂不引入 Spring Security，留作接入 SSO 时的演进方向。</li></ul>
  <h3>8 协作与排期过程</h3>
  <ul><li>登录/权限规则与产品确认后落地；与前端约定 401 跳登录、白名单路径与接口评审同步。</li></ul>
  <h3>9 复盘与可复用经验</h3>
  <ul><li><strong>够用即止</strong>：单系统 JWT 拦截器足够就不强行上重型安全框架。</li><li><strong>知道边界</strong>：清楚自研方案在 OAuth2/SSO 面前的天花板。</li></ul>
  <h3>10 面试讲法</h3>
  <p class="key-sentence">"DCP-RMP 我用自研 JWT 拦截器做登录态和权限，足够当前规模；我也对比学过 Spring Security 过滤器链，能讲清什么时候该演进到 OAuth2/SSO。"</p>
""")

# 14 MyBatisPlus real (选型对比)
R["07_后端开发/14_MyBatisPlus与SpringDataJPA【基础】.html"] = (REAL, """
  <h3>1 项目背景</h3>
  <p class="lead"><b>一句话定位</b>：DCP-RMP 与源启持久层用原生 MyBatis；本节基于真实 MyBatis 实践，做 MyBatis-Plus / JPA 的选型对比。</p>
  <ul><li><strong>业务量级</strong>：大量单表 CRUD + 部分复杂多表/动态 SQL。</li></ul>
  <h3>2 我的角色与职责</h3>
  <ul><li><strong>分工</strong>：写原生 MyBatis Mapper/XML；评估新模块是否改用 MyBatis-Plus 减少样板。</li></ul>
  <h3>3 技术栈</h3>
  <ul><li><strong>现状</strong>：SpringBoot 3 + MyBatis；<b>对比对象</b>：MyBatis-Plus（增强 MyBatis）、Spring Data JPA（全自动）。</li></ul>
  <h3>4 落地设计</h3>
  <ul>
    <li><strong>结论</strong>：复杂多表/报表留原生 MyBatis；标准单表 CRUD 若量大，MyBatis-Plus 可零 SQL，且与原生无缝混用。</li>
    <li><strong>不选 JPA 的理由</strong>：项目复杂动态 SQL 多，不能放弃 SQL 控制力。</li>
  </ul>
  <h3>5 关键实现要点</h3>
<pre class="code" data-lang="java"><code>// 原生 MyBatis：复杂查询仍自己写 XML（当前做法）
List&lt;ReqVO&gt; listVo(@Param("status") String status);

// 若引入 MP：单表 CRUD 零 SQL，复杂查询保留上面的 XML（选型对比）
public interface ReqMapper extends BaseMapper&lt;Req&gt; { }</code></pre>
  <h3>6 真实问题与解法</h3>
  <ul>
    <li><span class="tag-pit">坑</span><strong>MP 与 XML 方法 id 冲突</strong>：同名方法启动报错——命名避让。</li>
    <li><span class="tag-point">要点</span><strong>分页插件要注册</strong>：MP 分页需注册拦截器才生效。</li>
  </ul>
  <h3>7 量化成果</h3>
  <ul><li>评估可省去约六成单表 CRUD 的样板 XML（估算）；判定现有稳定系统不推翻，作为新模块默认选择。</li></ul>
  <h3>8 协作与排期过程</h3>
  <ul><li>选型结论与后端团队达成一致：保持原生 MyBatis，新模块按团队约定再决定是否引入 MP。</li></ul>
  <h3>9 复盘与可复用经验</h3>
  <ul><li><strong>便捷 ORM 只接管单表</strong>：复杂 SQL 永远保留手写。</li><li><strong>选型看 SQL 控制力需求</strong>。</li></ul>
  <h3>10 面试讲法</h3>
  <p class="key-sentence">"DCP-RMP/源启用原生 MyBatis，我做过 MP 与 JPA 的选型：保留复杂 SQL 控制力，单表 CRUD 才交给 MP，不盲目全自动。"</p>
""")

print("part B entries:", len(R))
for rel, (toc, body) in R.items():
    fp = os.path.join(ROOT, rel.replace("/", os.sep))
    html = io.open(fp, encoding="utf-8").read()
    html, n1 = re.subn(r'<li><a href="#sec5">[^<]*</a></li>',
                       '<li><a href="#sec5">%s</a></li>' % toc, html, count=1)
    new_block = '<section id="sec5" class="card">\n  <h2><span class="num">5</span>%s</h2>\n%s\n' % (toc, body)
    html, n2 = re.subn(r'<section id="sec5".*?(?=<section id="sec6")',
                       new_block, html, count=1, flags=re.S)
    io.open(fp, "w", encoding="utf-8", newline="\n").write(html)
    print(("OK " if n1 == 1 and n2 == 1 else "CHECK ") + rel, "toc=%d sec5=%d" % (n1, n2))
