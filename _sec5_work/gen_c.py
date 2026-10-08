# -*- coding: utf-8 -*-
import io, re, os
ROOT = r"C:\Users\Administrator\Doubao\chats\2026-10-06\new-chat-1\技术栈详解"
R = {}
REAL = "实战项目经验（真实项目落地）"
DEMO = "实战项目经验（自学 + 自建 Demo）"

# 01 MySQL【深入】 real
R["08_数据库与建模/01_MySQL【深入】.html"] = (REAL, """
  <h3>1 项目背景</h3>
  <p class="lead"><b>一句话定位</b>：DCP-RMP 与源启的业务数据落在 MySQL，表设计、字段类型、索引直接决定接口性能。</p>
  <ul><li><strong>业务量级</strong>：需求/团队/配置/权限等核心表，读多写少，列表查询频繁（估算）。</li></ul>
  <h3>2 我的角色与职责</h3>
  <ul><li><strong>分工</strong>：参与建表与字段类型选择，为高频查询设计索引，配合慢查询排查。</li></ul>
  <h3>3 技术栈</h3>
  <ul><li><strong>组合</strong>：MySQL（InnoDB 引擎）+ MyBatis + 应用层缓存 Redis。</li></ul>
  <h3>4 落地设计</h3>
  <ul>
    <li><strong>字段类型</strong>：状态/枚举用短 varchar/tinyint，时间用 datetime，金额用 decimal 不用 float。</li>
    <li><strong>字符集</strong>：统一 utf8mb4，避免 emoji/生僻字乱码。</li>
    <li><strong>索引</strong>：按高频 where/order by 建联合索引，遵循最左前缀。</li>
  </ul>
  <h3>5 关键实现要点</h3>
<pre class="code" data-lang="sql"><code>CREATE TABLE t_requirement (
  id        BIGINT PRIMARY KEY AUTO_INCREMENT,
  title     VARCHAR(128) NOT NULL,
  status    VARCHAR(16)  NOT NULL,
  team_id   BIGINT       NOT NULL,
  create_time DATETIME   NOT NULL,
  KEY idx_status_team (status, team_id)   -- 高频按状态+团队查
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;</code></pre>
  <h3>6 真实问题与解法</h3>
  <ul>
    <li><span class="tag-pit">坑</span><strong>索引没命中</strong>：列表查询全表扫——explain 发现 type=ALL，按查询条件补联合索引后走 ref。</li>
    <li><span class="tag-pit">坑</span><strong>隐式类型转换</strong>：字符串字段用数字去查，索引失效——保持类型一致。</li>
    <li><span class="tag-point">要点</span><strong>范式与反范式</strong>：展示用的团队名高频 join，必要时冗余字段换读性能。</li>
  </ul>
  <h3>7 量化成果</h3>
  <ul><li>高频列表查询补联合索引后从全表扫降到走索引（约秒级→毫秒级，随数据量，估算）。</li></ul>
  <h3>8 协作与排期过程</h3>
  <ul><li>表结构与 DBA/后端评审；新增查询条件时同步评估是否要加索引，避免事后补。</li></ul>
  <h3>9 复盘与可复用经验</h3>
  <ul><li><strong>索引跟着查询走</strong>：先有高频 SQL 再设计索引。</li><li><strong>类型与字符集统一</strong>：utf8mb4 + 无隐式转换。</li></ul>
  <h3>10 面试讲法</h3>
  <p class="key-sentence">"DCP-RMP/源启的 MySQL 表我按高频查询设计联合索引、统一 utf8mb4，靠 explain 抓全表扫补索引，把列表查询从秒级优化到毫秒级。"</p>
""")

# 02 MySQL进阶 索引与SQL优化【深入】 real
R["08_数据库与建模/02_MySQL进阶_索引与SQL优化【深入】.html"] = (REAL, """
  <h3>1 项目背景</h3>
  <p class="lead"><b>一句话定位</b>：电力大屏历史告警数据量大，按"时间范围 + 告警状态"组合查询与列表深分页逐渐变慢。</p>
  <ul><li><strong>业务量级</strong>：告警表随时间累积到百万~千万行（估算），大屏与运维要查最近告警并翻页。</li></ul>
  <h3>2 我的角色与职责</h3>
  <ul><li><strong>分工</strong>：负责告警查询的慢 SQL 分析、索引设计与分页方式改造。</li></ul>
  <h3>3 技术栈</h3>
  <ul><li><strong>组合</strong>：MySQL InnoDB + 应用层；慢查询日志 + explain 作为分析工具。</li></ul>
  <h3>4 落地设计</h3>
  <ul>
    <li><strong>组合索引</strong>：为"时间范围 + 状态"建联合索引，让常用过滤命中。</li>
    <li><strong>覆盖索引</strong>：列表只取几列时，让索引覆盖查询，避免回表。</li>
    <li><strong>深分页</strong>：<code>LIMIT 100000,20</code> 翻页慢，改游标/延迟关联。</li>
  </ul>
  <h3>5 关键实现要点</h3>
<pre class="code" data-lang="sql"><code>-- 组合索引：(level, ts) 命中"按级别过滤 + 时间范围"
SELECT id, ts, level, title
FROM alarm
WHERE level = ? AND ts &gt;= ? AND ts &lt; ?
ORDER BY ts DESC LIMIT 20;

-- 深分页：游标分页（记住上一页最后一条 ts/id），避免 OFFSET 扫大量行
WHERE (ts, id) &lt; (?, ?) ORDER BY ts DESC, id DESC LIMIT 20;</code></pre>
  <h3>6 真实问题与解法</h3>
  <ul>
    <li><span class="tag-pit">坑</span><strong>深分页越翻越慢</strong>：<code>LIMIT 100000,20</code> 要先扫前 10 万行再丢弃——改游标分页，翻到后面耗时稳定。</li>
    <li><span class="tag-pit">坑</span><strong>order by 不在索引</strong>：filesort 拖慢——把排序列纳入索引顺序。</li>
    <li><span class="tag-point">要点</span><strong>索引下推 ICP</strong>：回表前先用索引列过滤，减少回表行数。</li>
  </ul>
  <h3>7 量化成果</h3>
  <ul><li>告警组合查询走索引后由全表扫降到毫秒级；深分页翻到靠后页从约数百毫秒级（估算）稳定到几十毫秒级。</li></ul>
  <h3>8 协作与排期过程</h3>
  <ul><li>慢查询从慢日志定位，与前端确认是否真需要翻深页（否则加时间范围收敛）；索引变更在低峰上线。</li></ul>
  <h3>9 复盘与可复用经验</h3>
  <ul><li><strong>先 explain 再优化</strong>：不凭感觉加索引。</li><li><strong>深分页用游标</strong>：OFFSET 深翻是已知坑。</li></ul>
  <h3>10 面试讲法</h3>
  <p class="key-sentence">"大屏告警表我按时间+状态建联合索引、用覆盖索引减少回表，并把深分页从 OFFSET 改游标分页，靠 explain 定位全表扫和 filesort。"</p>
""")

# 03 MySQL事务与锁【标准】 real
R["08_数据库与建模/03_MySQL事务与锁【标准】.html"] = (REAL, """
  <h3>1 项目背景</h3>
  <p class="lead"><b>一句话定位</b>：DCP-RMP 需求要走"提交→评审→通过/驳回"状态流转，一个动作里要同时改状态、写流转记录，且可能并发抢同一条。</p>
  <ul><li><strong>业务量级</strong>：多人同时处理同一需求时存在并发更新（估算）。</li></ul>
  <h3>2 我的角色与职责</h3>
  <ul><li><strong>分工</strong>：用事务包裹状态流转，处理并发更新冲突与隔离级别选择。</li></ul>
  <h3>3 技术栈</h3>
  <ul><li><strong>组合</strong>：Spring @Transactional + MySQL InnoDB（默认 REPEATABLE READ）。</li></ul>
  <h3>4 落地设计</h3>
  <ul>
    <li><strong>事务边界</strong>：一次状态流转 = 改需求状态 + 插流转记录，放一个事务。</li>
    <li><strong>并发控制</strong>：更新带乐观锁版本号或 <code>where status=期望态</code>，避免两人同时改覆盖。</li>
  </ul>
  <h3>5 关键实现要点</h3>
<pre class="code" data-lang="java"><code>@Transactional(rollbackFor = Exception.class)
public void review(Long id, String next) {
    int rows = reqMapper.casUpdateStatus(id, "REVIEW", next); // where status=期望态
    if (rows == 0) throw new BizException("状态已被他人变更", 40909);
    flowLogMapper.insert(new FlowLog(id, "REVIEW", next));
}</code></pre>
  <h3>6 真实问题与解法</h3>
  <ul>
    <li><span class="tag-pit">坑</span><strong>丢失更新</strong>：两人同时读到旧状态再各写回，后写覆盖先写——用条件更新 where status=期望态兜底。</li>
    <li><span class="tag-pit">坑</span><strong>死锁</strong>：两个事务以不同顺序更新多行导致死锁——固定加锁顺序，缩小事务。</li>
    <li><span class="tag-point">要点</span><strong>隔离级别够用即可</strong>：业务用默认 RR，幻读风险点用条件更新规避。</li>
  </ul>
  <h3>7 量化成果</h3>
  <ul><li>并发改同一需求不再互相覆盖，冲突时返回明确提示让用户刷新（冲突率极低，估算）。</li></ul>
  <h3>8 协作与排期过程</h3>
  <ul><li>状态机与产品确认；冲突返回 409 后前端引导刷新，与前端约定错误码。</li></ul>
  <h3>9 复盘与可复用经验</h3>
  <ul><li><strong>状态流转必带条件</strong>：乐观条件更新防丢失更新。</li><li><strong>事务尽量短</strong>：减少锁持有时间与死锁面。</li></ul>
  <h3>10 面试讲法</h3>
  <p class="key-sentence">"DCP-RMP 需求状态流转我用事务包住状态变更+流转记录，用 where status=期望态的条件更新防并发丢失更新，也处理过加锁顺序导致的死锁。"</p>
""")

# 04 Oracle【深入】 demo
R["08_数据库与建模/04_Oracle【深入】.html"] = (DEMO, """
  <div class="warn-box"><b>诚实说明：</b>本人简历项目均以 MySQL 为主，未列 Oracle 项目。本节为 Oracle 与 MySQL 差异对照的自学走读笔记（安装/基础语法/特性对比验证），非企业履历。</div>
  <h3>1 自学背景与动机</h3>
  <p class="lead"><b>一句话定位</b>：补"从 MySQL 切到 Oracle 要改哪些习惯"的认知，应对企业大型系统可能用到 Oracle 的场景。</p>
  <ul><li><strong>缺口</strong>：分页、序列、锁、数据字典都和 MySQL 不一样，需要对照验证。</li></ul>
  <h3>2 搭建的 demo 是什么</h3>
  <ul>
    <li><strong>结构</strong>：本地 Oracle（或免费 XE 版）建一张业务表，把 MySQL 里跑过的 CRUD 用 Oracle 语法重写对照。</li>
    <li><strong>规模</strong>：单表 + 序列 + 分页查询，验证差异点。</li>
  </ul>
  <h3>3 落地步骤</h3>
<pre class="code" data-lang="sql"><code>-- Oracle：自增靠序列 + 触发器，不是 AUTO_INCREMENT
CREATE SEQUENCE seq_req START WITH 1 INCREMENT BY 1;
INSERT INTO req(id, title) VALUES(seq_req.NEXTVAL, '评审');

-- Oracle 分页：用 ROWNUM / 子查询（MySQL 是 LIMIT）
SELECT * FROM (
  SELECT t.*, ROWNUM rn FROM req t WHERE ROWNUM &lt;= 20
) WHERE rn &gt; 0;</code></pre>
  <h3>4 自学过程中遇到的坑与解决</h3>
  <ul>
    <li><span class="tag-pit">坑</span><strong>分页语法不同</strong>：习惯了 LIMIT 10,20，Oracle 要套 ROWNUM 子查询——改写并验证结果一致。</li>
    <li><span class="tag-pit">坑</span><strong>空字符串即 NULL</strong>：Oracle 里 <code>''</code> 等价 NULL，判空逻辑要注意。</li>
    <li><span class="tag-point">要点</span><strong>共享池/SGA</strong>：调优思路与 MySQL buffer pool 不同，要先理解 SGA/PGA。</li>
  </ul>
  <h3>5 成果</h3>
  <ul><li>能对照讲清 Oracle 与 MySQL 在分页、序列、锁、调优（SGA/PGA）上的关键差异，迁移 SQL 时知道改哪里。</li></ul>
  <h3>6 与真实项目的差异</h3>
  <ul><li>本地单机验证，未上生产；真实大型 Oracle 系统的 RAC/表空间/权限模型仅作概念了解。</li></ul>
  <h3>7 面试讲法</h3>
  <p class="key-sentence">"我用本地 Oracle 把 MySQL 常用 CRUD 对照重写过，清楚序列、ROWNUM 分页、空串即 NULL 这些差异，迁移 SQL 能快速上手。"</p>
""")

# 05 Redis缓存【标准】 real
R["08_数据库与建模/05_Redis缓存【标准】.html"] = (REAL, """
  <h3>1 项目背景</h3>
  <p class="lead"><b>一句话定位</b>：DCP-RMP 用 Redis 做热点数据缓存、登录会话/黑名单与计数器，减轻 MySQL 压力。</p>
  <ul><li><strong>业务量级</strong>：字典/权限/热点配置读多写少；登录态与计数频繁访问。</li></ul>
  <h3>2 我的角色与职责</h3>
  <ul><li><strong>分工</strong>：接入 Redis，设计缓存 key、过期策略与缓存更新方式。</li></ul>
  <h3>3 技术栈</h3>
  <ul><li><strong>组合</strong>：SpringBoot Data Redis + Redisson + MySQL。</li></ul>
  <h3>4 落地设计</h3>
  <ul>
    <li><strong>热点缓存</strong>：字典/配置先查缓存，miss 再查库并回写。</li>
    <li><strong>会话/黑名单</strong>：JWT 黑名单、refresh token 存 Redis，带过期时间。</li>
    <li><strong>计数</strong>：浏览量/计数用 incr，不落库实时算。</li>
  </ul>
  <h3>5 关键实现要点</h3>
<pre class="code" data-lang="java"><code>public Dict getDict(String code) {
    String key = "dict:" + code;
    String json = redis.get(key);
    if (json != null) return JSON.parse(json, Dict.class);
    Dict d = dictMapper.selectByCode(code);   // miss 查库
    redis.setex(key, 3600, JSON.stringify(d)); // 回写 + 1h 过期
    return d;
}</code></pre>
  <h3>6 真实问题与解法</h3>
  <ul>
    <li><span class="tag-pit">坑</span><strong>缓存与库不一致</strong>：更新库后忘了删缓存——写操作后删缓存（Cache-Aside）而非更新缓存。</li>
    <li><span class="tag-pit">坑</span><strong>序列化</strong>：对象直接存 JDK 序列化体积大、跨语言不可读——用 JSON 字符串。</li>
    <li><span class="tag-point">要点</span><strong>必设过期</strong>：key 不设 TTL 会无限堆积。</li>
  </ul>
  <h3>7 量化成果</h3>
  <ul><li>热点字典查询大部分命中缓存，MySQL 读压力下降（缓存命中率约九成，估算）。</li></ul>
  <h3>8 协作与排期过程</h3>
  <ul><li>key 命名规范后端统一；缓存失效策略与数据变更点一起评审。</li></ul>
  <h3>9 复盘与可复用经验</h3>
  <ul><li><strong>Cache-Aside + 删缓存</strong>：读穿透、写删缓存。</li><li><strong>JSON 序列化 + TTL</strong>。</li></ul>
  <h3>10 面试讲法</h3>
  <p class="key-sentence">"DCP-RMP 我用 Redis 做字典缓存、JWT 黑名单和计数，Cache-Aside 读穿透写删缓存，踩过库更新后缓存不一致和序列化的坑。"</p>
""")

# 06 Redis进阶 Redisson【深入】 real
R["08_数据库与建模/06_Redis进阶_缓存策略与分布式锁【深入】.html"] = (REAL, """
  <h3>1 项目背景</h3>
  <p class="lead"><b>一句话定位</b>：DCP-RMP 需求并发操作（如同一需求被多人同时处理、幂等提交）需要分布式锁保证一致性，用 Redisson。</p>
  <ul><li><strong>业务量级</strong>：后端虽为单体部署多实例时，临界区操作必须跨实例互斥（估算多实例）。</li></ul>
  <h3>2 我的角色与职责</h3>
  <ul><li><strong>分工</strong>：用 Redisson 实现可重入分布式锁，处理需求并发提交与接口幂等。</li></ul>
  <h3>3 技术栈</h3>
  <ul><li><strong>组合</strong>：SpringBoot + Redisson（基于 Redis）+ MySQL。</li></ul>
  <h3>4 落地设计</h3>
  <ul>
    <li><strong>锁粒度</strong>：按需求 id 加锁 <code>lock:req:{id}</code>，同一需求串行处理，不同需求并行。</li>
    <li><strong>看门狗</strong>：用 Redisson 默认看门狗自动续期，避免业务没执行完锁先过期。</li>
    <li><strong>幂等</strong>：关键提交接口先抢锁/查幂等键，防重复提交。</li>
  </ul>
  <h3>5 关键实现要点</h3>
<pre class="code" data-lang="java"><code>RLock lock = redisson.getLock("lock:req:" + reqId);
try {
    if (!lock.tryLock(3, 30, TimeUnit.SECONDS)) {
        throw new BizException("该需求正在被处理，请稍后", 40909);
    }
    // 临界区：查最新状态 → 校验 → 更新
    doReview(reqId, cmd);
} finally {
    if (lock.isHeldByCurrentThread()) lock.unlock();  // 只解自己持有的锁
}</code></pre>
  <h3>6 真实问题与解法</h3>
  <ul>
    <li><span class="tag-pit">坑</span><strong>手写 setnx 锁不释放</strong>：进程持锁后崩溃没删 key——用 Redisson 带过期 + 看门狗，不手写裸 setnx。</li>
    <li><span class="tag-pit">坑</span><strong>解锁解到别人的锁</strong>：锁过期后被别人抢到，自己 finally 误删——<code>isHeldByCurrentThread</code> 判断。</li>
    <li><span class="tag-point">要点</span><strong>锁内别做长事务</strong>：持锁做重活会拉长临界区，锁内只做必要更新。</li>
  </ul>
  <h3>7 量化成果</h3>
  <ul><li>同一需求并发提交不再出现状态覆盖，重复提交被挡在锁/幂等层（冲突被拦截，估算）。</li></ul>
  <h3>8 协作与排期过程</h3>
  <ul><li>与前端约定 409"正在处理"提示并引导刷新；锁 key 规范与超时参数后端统一评审。</li></ul>
  <h3>9 复盘与可复用经验</h3>
  <ul><li><strong>用成熟客户端</strong>：Redisson 而非手写 setnx，续期/可重入都解决了。</li><li><strong>锁内要短</strong>。</li></ul>
  <h3>10 面试讲法</h3>
  <p class="key-sentence">"DCP-RMP 我用 Redisson 按需求 id 加可重入锁、靠看门狗续期保证并发一致性，踩过手写 setnx 不释放和误删别人锁的坑，所以一律用成熟客户端。"</p>
""")

# 07 高可用与分库分表【标准】 real
R["08_数据库与建模/07_数据库高可用与分库分表【标准】.html"] = (REAL, """
  <h3>1 项目背景</h3>
  <p class="lead"><b>一句话定位</b>：DCP-RMP 用单主 MySQL；大屏项目群的历史告警数据随时间累积，需要高可用与归档/扩容方案评估。</p>
  <ul><li><strong>业务量级</strong>：核心业务单库可承载；历史告警表持续增长（估算到百万~千万行）。</li></ul>
  <h3>2 我的角色与职责</h3>
  <ul><li><strong>分工</strong>：评估主从复制/读写分离与历史数据归档方案；大屏历史数据定期归档。</li></ul>
  <h3>3 技术栈</h3>
  <ul><li><strong>组合</strong>：MySQL 主从（评估）+ 读写分离思路；历史数据归档脚本；分库分表 ShardingSphere 仅作方案评估。</li></ul>
  <h3>4 落地设计</h3>
  <ul>
    <li><strong>高可用</strong>：评估一主多从，读请求走从库、写走主库，主挂提升从库。</li>
    <li><strong>归档优先</strong>：历史告警按月归档到归档表/冷存储，在线表只留近期数据，而不是一开始就分库分表。</li>
  </ul>
  <h3>5 关键实现要点</h3>
<pre class="code" data-lang="sql"><code>-- 按月归档：把 N 个月前的告警搬入归档表，在线表只保留近期
INSERT INTO alarm_archive_2026_06
SELECT * FROM alarm WHERE ts &lt; '2026-07-01';
DELETE FROM alarm WHERE ts &lt; '2026-07-01';</code></pre>
  <h3>6 真实问题与解法</h3>
  <ul>
    <li><span class="tag-pit">坑</span><strong>过早分库分表</strong>：数据量还没到就引入分片，复杂度翻倍——先归档、读写分离，分片留作扩容手段。</li>
    <li><span class="tag-pit">坑</span><strong>归档大事务锁表</strong>：一次搬太多行长事务锁表——分批小事务搬。</li>
  </ul>
  <h3>7 量化成果</h3>
  <ul><li>在线告警表体积受控，近期查询不受历史数据拖累；主从/读写分离作为高可用基线方案（归档分批，估算）。</li></ul>
  <h3>8 协作与排期过程</h3>
  <ul><li>归档任务在低峰定时跑；高可用方案与运维/DBA 一起评估主从切换。</li></ul>
  <h3>9 复盘与可复用经验</h3>
  <ul><li><strong>先归档再分片</strong>：能用冷热分离解决就别上分片。</li><li><strong>分批处理大迁移</strong>。</li></ul>
  <h3>10 面试讲法</h3>
  <p class="key-sentence">"我给大屏历史告警做按月归档、评估主从读写分离，坚持先归档再谈分库分表，避免过早引入分片复杂度。"</p>
""")

# 08 PowerDesigner【基础】 real
R["08_数据库与建模/08_PowerDesigner数据库建模【基础】.html"] = (REAL, """
  <h3>1 项目背景</h3>
  <p class="lead"><b>一句话定位</b>：DCP-RMP/需求平台早期用 PowerDesigner 做 ER 建模，把业务概念转成数据库物理表结构。</p>
  <ul><li><strong>业务量级</strong>：需求/团队/权限/流转等核心实体，表关系需要先画清楚再落地。</li></ul>
  <h3>2 我的角色与职责</h3>
  <ul><li><strong>分工</strong>：参与概念模型设计、转物理模型，正向工程生成建表语句。</li></ul>
  <h3>3 技术栈</h3>
  <ul><li><strong>组合</strong>：PowerDesigner（CDM→LDM→PDM）+ MySQL。</li></ul>
  <h3>4 落地设计</h3>
  <ul>
    <li><strong>概念模型</strong>：先画实体与关系（需求—团队—用户），不纠结字段类型。</li>
    <li><strong>逻辑→物理</strong>：把概念模型转成物理模型，指定 MySQL 方言与字段类型，正向工程导出 DDL。</li>
  </ul>
  <h3>5 关键实现要点</h3>
<pre class="code" data-lang="text"><code>流程：概念模型 CDM（实体+关系）
   → 逻辑模型 LDM（加主键/属性）
   → 物理模型 PDM（MySQL 方言、字段类型）
   → 正向工程生成建表 SQL → 反向工程可由库回刷模型</code></pre>
  <h3>6 真实问题与解法</h3>
  <ul>
    <li><span class="tag-pit">坑</span><strong>模型与库脱节</strong>：直接改库后没回刷模型，文档过时——改动后用反向工程同步。</li>
    <li><span class="tag-point">要点</span><strong>外键关系先想清</strong>：建模阶段理清一对多/多对多，比后期改表便宜。</li>
  </ul>
  <h3>7 量化成果</h3>
  <ul><li>建表前 ER 关系一次理清，减少后期大改表结构的返工（估算）。</li></ul>
  <h3>8 协作与排期过程</h3>
  <ul><li>模型在评审阶段与产品/DBA 确认，确认后再出 DDL 建表。</li></ul>
  <h3>9 复盘与可复用经验</h3>
  <ul><li><strong>先模型后建表</strong>：关系理清再落地。</li><li><strong>模型随库同步</strong>。</li></ul>
  <h3>10 面试讲法</h3>
  <p class="key-sentence">"需求平台我用 PowerDesigner 走 概念→逻辑→物理 模型，正向工程出 DDL，靠反向工程保持模型与库一致。"</p>
""")

# 09 ES demo
R["08_数据库与建模/09_Elasticsearch搜索引擎【标准】.html"] = (DEMO, """
  <div class="warn-box"><b>定位说明：</b>本人简历项目未实际部署 Elasticsearch。本节为本地 ES 检索自学 demo，验证索引/分词/查询/聚合，并模拟 MySQL 数据同步。</div>
  <h3>1 自学背景与动机</h3>
  <p class="lead"><b>一句话定位</b>：补"MySQL like 模糊查为什么慢、ES 倒排索引怎么解决"的认知，对应大屏告警/日志检索规划。</p>
  <ul><li><strong>缺口</strong>：一直用 MySQL，没实际碰过分词与倒排索引。</li></ul>
  <h3>2 搭建的 demo 是什么</h3>
  <ul>
    <li><strong>结构</strong>：本地单节点 ES，建告警索引（title 用 IK 分词），灌入一批模拟告警，跑全文查询 + 按天聚合。</li>
    <li><strong>规模</strong>：万级模拟文档，验证查询与聚合延迟。</li>
  </ul>
  <h3>3 落地步骤</h3>
<pre class="code" data-lang="json"><code>PUT /alarm-index
{ "mappings": { "properties": {
    "title": { "type": "text", "analyzer": "ik_max_word" },
    "level": { "type": "keyword" },
    "ts":    { "type": "date" }
}}}</code></pre>
<pre class="code" data-lang="json"><code>GET /alarm-index/_search
{ "query": { "match": { "title": "监控" } },
  "aggs": { "by_day": { "date_histogram": { "field": "ts", "calendar_interval": "day" } } } }</code></pre>
  <h3>4 自学过程中遇到的坑与解决</h3>
  <ul>
    <li><span class="tag-pit">坑</span><strong>中文没分词</strong>：默认分析器按单字切，召回不准——装 IK 分词器并在 mapping 指定。</li>
    <li><span class="tag-pit">坑</span><strong>写完立即可查</strong>：写入后查不到——ES 近实时，等约 1 秒 refresh。</li>
  </ul>
  <h3>5 成果</h3>
  <ul><li>跑通建索引→分词→match 查询→聚合，验证了"按词查"比 MySQL like 快；理解与 MySQL 的分工。</li></ul>
  <h3>6 与真实项目的差异</h3>
  <ul><li>单节点无集群/监控；真实大屏告警检索是规划中的演进方向，数据同步需 MQ 异步。</li></ul>
  <h3>7 面试讲法</h3>
  <p class="key-sentence">"我本地用 ES 建告警索引、装 IK 分词、跑 match+聚合 demo，理解倒排索引为什么比 like 快，也清楚它和 MySQL 的分工与近实时特性。"</p>
""")

# 10 MongoDB demo
R["08_数据库与建模/10_MongoDB与NoSQL【基础】.html"] = (DEMO, """
  <div class="warn-box"><b>定位说明：</b>本人简历项目以 MySQL 为主，未实际使用 MongoDB。本节为文档模型 CRUD 自学 demo 与关系型选型对比。</div>
  <h3>1 自学背景与动机</h3>
  <p class="lead"><b>一句话定位</b>：补"文档型 NoSQL 怎么存、和关系型怎么选"的认知。</p>
  <ul><li><strong>缺口</strong>：一直用表结构，不清楚嵌套文档、复制集分片的实际用法。</li></ul>
  <h3>2 搭建的 demo 是什么</h3>
  <ul>
    <li><strong>结构</strong>：本地 MongoDB，建一个需求文档集合（内嵌评论数组），做 CRUD 与查询，对比同样数据在 MySQL 要拆几张表。</li>
  </ul>
  <h3>3 落地步骤</h3>
<pre class="code" data-lang="json"><code>db.requirement.insertOne({
  title: "评审需求", status: "REVIEW",
  comments: [ { user: "张三", text: "同意" } ]   // 内嵌评论，无需 join
})
db.requirement.find({ status: "REVIEW" })</code></pre>
  <h3>4 自学过程中遇到的坑与解决</h3>
  <ul>
    <li><span class="tag-pit">坑</span><strong>查全集合</strong>：没建索引 find 全扫——为 status 等高频字段建索引。</li>
    <li><span class="tag-point">要点</span><strong>无 schema 不等于不设计</strong>：字段乱存后期迁移困难，仍要约定结构。</li>
  </ul>
  <h3>5 成果</h3>
  <ul><li>跑通文档 CRUD，能讲清"内嵌 vs 拆表"的取舍与复制集/分片的作用。</li></ul>
  <h3>6 与真实项目的差异</h3>
  <ul><li>单机 demo 无复制集/分片；真实选型上核心交易数据仍留 MySQL。</li></ul>
  <h3>7 面试讲法</h3>
  <p class="key-sentence">"我本地跑过 MongoDB 文档 CRUD，理解嵌套文档与复制集分片，能讲清什么时候用 NoSQL、什么时候必须留关系型。"</p>
""")

# 11 ClickHouse demo
R["08_数据库与建模/11_ClickHouse_OLAP分析【标准】.html"] = (DEMO, """
  <div class="warn-box"><b>定位说明：</b>本人简历大屏项目群未实际部署 ClickHouse。本节为列存聚合自学 demo，挂"大屏告警海量聚合"场景规划，非企业履历。</div>
  <h3>1 自学背景与动机</h3>
  <p class="lead"><b>一句话定位</b>：补"MySQL group by 在亿级告警上变慢，列式数据库怎么做到秒级聚合"的认知。</p>
  <ul><li><strong>缺口</strong>：一直用 MySQL，没碰过列式存储与向量化执行。</li></ul>
  <h3>2 搭建的 demo 是什么</h3>
  <ul>
    <li><strong>结构</strong>：本地 ClickHouse，建 MergeTree 告警表（按月分区、级别 LowCardinality），灌入模拟海量告警数据，跑按天+级别聚合。</li>
    <li><strong>规模</strong>：百万级模拟行，对比 MySQL 同查询耗时。</li>
  </ul>
  <h3>3 落地步骤</h3>
<pre class="code" data-lang="sql"><code>CREATE TABLE alarm (
  ts DateTime, deviceId String,
  level LowCardinality(String), title String
) ENGINE=MergeTree PARTITION BY toYYYYMM(ts) ORDER BY (deviceId, ts);

SELECT toDate(ts) day, level, count()
FROM alarm WHERE ts &gt; now()-INTERVAL 30 DAY
GROUP BY day, level ORDER BY day;</code></pre>
  <h3>4 自学过程中遇到的坑与解决</h3>
  <ul>
    <li><span class="tag-pit">坑</span><strong>逐条写入</strong>：逐行 insert 产生大量小 part、查询变慢——攒批导入。</li>
    <li><span class="tag-point">要点</span><strong>按时间分区</strong>：时间范围查询才能裁剪分区。</li>
  </ul>
  <h3>5 成果</h3>
  <ul><li>验证了列式 + 分区裁剪下聚合远快于 MySQL 全表 group by；理解它与 MySQL/ES 的分工。</li></ul>
  <h3>6 与真实项目的差异</h3>
  <ul><li>单机 demo 无集群/无物化视图；真实大屏告警聚合是规划方向，需数据同步链路。</li></ul>
  <h3>7 面试讲法</h3>
  <p class="key-sentence">"我本地用 ClickHouse 建分区 MergeTree 表灌入模拟告警、跑按天聚合，亲手验证列存比 MySQL group by 快得多，也清楚它只做分析侧、不做业务库。"</p>
""")

print("part C entries:", len(R))
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
