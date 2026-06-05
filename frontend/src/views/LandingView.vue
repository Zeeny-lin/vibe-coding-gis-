<template>
  <div class="landing-view">
    <!-- 顶部导航栏 -->
    <header class="landing-header">
      <div class="logo-area">
        <span class="logo-icon">🌊</span>
        <div class="logo-text">
          <h1>莆田市市情WebGIS系统</h1>
          <span class="tagline">数字莆田 · 智慧城市</span>
        </div>
      </div>
      <nav class="header-nav">
        <router-link to="/home" class="nav-btn primary">进入地图系统</router-link>
      </nav>
    </header>

    <!-- 主视觉区域 -->
    <section class="hero-section">
      <div class="hero-content">
        <h2 class="hero-title">
          <span class="title-line">妈祖故里</span>
          <span class="title-line accent">进士之乡</span>
        </h2>
        <p class="hero-desc">
          莆田，古称"兴化"，素有"海滨邹鲁"之美誉。这里是妈祖文化的发源地，
          是中华文明与海洋文化交融的璀璨明珠，承载着千年文脉与现代发展的交响乐章。
        </p>

        <!-- 装饰性搜索栏 -->
        <div class="hero-search-bar">
          <input 
            type="text" 
            class="search-input" 
            v-model="searchQuery"
            @keyup.enter="handleSearch"
            placeholder="搜索目的地 / 文化遗产 / 产业数据..." 
          />
          <div class="search-btn-icon" @click="handleSearch">
            <el-icon><Search /></el-icon>
          </div>
        </div>

        <div class="hero-stats">
          <div class="stat-item">
            <span class="stat-num">4119</span>
            <span class="stat-label">平方公里</span>
          </div>
          <div class="stat-item">
            <span class="stat-num">321</span>
            <span class="stat-label">常住人口（万）</span>
          </div>
          <div class="stat-item">
            <span class="stat-num">5</span>
            <span class="stat-label">行政区县</span>
          </div>
        </div>
      </div>
      <div class="hero-image">
        <div class="image-placeholder">
          <el-carousel trigger="click" height="300px" arrow="always">
            <el-carousel-item v-for="item in carouselImages" :key="item.name">
              <img :src="item.url" :alt="item.name" style="width: 100%; height: 100%; object-fit: cover;" />
              <div class="carousel-caption">{{ item.label }}</div>
            </el-carousel-item>
          </el-carousel>
        </div>
      </div>
    </section>

    <!-- 城市名片 -->
    <section class="city-intro">
      <h3 class="section-title">🏛️ 城市名片</h3>
      <div class="intro-cards">
        <div class="intro-card clickable-card" @click="openCityDetail('mazu')">
          <div class="card-image-wrapper">
            <img src="/images/cards/妈祖故里.jpg" alt="妈祖故里" />
          </div>
          <div class="card-content">
            <h4>妈祖故里</h4>
            <p>湄洲岛是妈祖文化的发源地，全球5000多座妈祖庙的祖庙所在地。每年吸引数百万海内外信众前来朝圣，是连接两岸文化的重要纽带。</p>
          </div>
          <span class="card-explore-hint">点击了解详情 →</span>
        </div>
        <div class="intro-card clickable-card" @click="openCityDetail('jinshi')">
          <div class="card-image-wrapper">
            <img src="/images/cards/culture.png" alt="进士之乡" />
          </div>
          <div class="card-content">
            <h4>进士之乡</h4>
            <p>莆田历史悠久，文化底蕴深厚，自古文风鼎盛。历史上涌现出2482位进士、21位状元，素有"进士之乡"的美誉。</p>
          </div>
          <span class="card-explore-hint">点击了解详情 →</span>
        </div>
        <div class="intro-card clickable-card" @click="openCityDetail('industry')">
          <div class="card-image-wrapper">
            <img src="/images/cards/产业名城.jpg" alt="产业名城" />
          </div>
          <div class="card-content">
            <h4>产业名城</h4>
            <p>莆田是中国鞋业之都、黄金珠宝之城、木雕之城。现代产业与传统工艺交相辉映，经济蓬勃发展。</p>
          </div>
          <span class="card-explore-hint">点击了解详情 →</span>
        </div>
        <div class="intro-card clickable-card" @click="openCityDetail('ecology')">
          <div class="card-image-wrapper">
            <img src="/images/cards/生态宜居.jpeg" alt="生态宜居" />
          </div>
          <div class="card-content">
            <h4>生态宜居</h4>
            <p>木兰溪治理是习近平生态文明思想的重要实践，从"水患之河"到"生态之河"，展现了绿色发展的莆田样本。</p>
          </div>
          <span class="card-explore-hint">点击了解详情 →</span>
        </div>
      </div>
    </section>

    <!-- 系统导航 -->
    <section class="system-nav">
      <h3 class="section-title">🗺️ 系统导航</h3>
      <div class="nav-grid">
        <router-link to="/home" class="nav-card">
          <div class="nav-icon" style="background: linear-gradient(135deg, #C41E3A, #9A1830)">🏠</div>
          <span>城市概况</span>
        </router-link>
        <router-link to="/tourism" class="nav-card">
          <div class="nav-icon" style="background: linear-gradient(135deg, #FFD700, #C5A000)">🎭</div>
          <span>文化旅游</span>
        </router-link>
        <router-link to="/transport" class="nav-card">
          <div class="nav-icon" style="background: linear-gradient(135deg, #2196F3, #1565C0)">🚛</div>
          <span>综合交通</span>
        </router-link>
        <router-link to="/population" class="nav-card">
          <div class="nav-icon" style="background: linear-gradient(135deg, #4CAF50, #2E7D32)">👥</div>
          <span>人口分布</span>
        </router-link>
        <router-link to="/service" class="nav-card">
          <div class="nav-icon" style="background: linear-gradient(135deg, #00BCD4, #00838F)">🏥</div>
          <span>公共服务</span>
        </router-link>
        <router-link to="/environment" class="nav-card">
          <div class="nav-icon" style="background: linear-gradient(135deg, #8BC34A, #558B2F)">🌿</div>
          <span>生态环境</span>
        </router-link>
      </div>
    </section>

    <!-- 政策文件导览 -->
    <section class="policy-section">
      <h3 class="section-title">📋 政策文件导览</h3>
      <p class="section-desc">查阅莆田市最新政务公开文件和政策信息</p>
      <div class="policy-grid">
        <a href="https://www.putian.gov.cn/" target="_blank" class="policy-card" @click.prevent="openPolicyLink('https://www.putian.gov.cn/', '莆田市人民政府门户网站')">
          <div class="policy-icon">🏛️</div>
          <div class="policy-info">
            <h5>莆田市人民政府</h5>
            <p>官方门户网站，政务公开信息</p>
          </div>
          <span class="policy-arrow">→</span>
        </a>
        <a href="https://www.putian.gov.cn/zwgk/" target="_blank" class="policy-card" @click.prevent="openPolicyLink('https://www.putian.gov.cn/zwgk/', '政务公开')">
          <div class="policy-icon">📄</div>
          <div class="policy-info">
            <h5>政务公开</h5>
            <p>政府信息公开、行政决策公开</p>
          </div>
          <span class="policy-arrow">→</span>
        </a>
        <a href="https://www.putian.gov.cn/zwfw/" target="_blank" class="policy-card" @click.prevent="openPolicyLink('https://www.putian.gov.cn/zwfw/', '政务服务')">
          <div class="policy-icon">📝</div>
          <div class="policy-info">
            <h5>政务服务</h5>
            <p>网上办事大厅、便民服务</p>
          </div>
          <span class="policy-arrow">→</span>
        </a>
        <a href="https://www.putian.gov.cn/ztzl/fwptcyfz/" target="_blank" class="policy-card" @click.prevent="openPolicyLink('https://www.putian.gov.cn/ztzl/', '专题专栏')">
          <div class="policy-icon">📊</div>
          <div class="policy-info">
            <h5>专题专栏</h5>
            <p>重点工作、民生实事、发展规划</p>
          </div>
          <span class="policy-arrow">→</span>
        </a>
        <a href="http://zjj.putian.gov.cn/" target="_blank" class="policy-card" @click.prevent="openPolicyLink('http://zjj.putian.gov.cn/', '住建局')">
          <div class="policy-icon">🏗️</div>
          <div class="policy-info">
            <h5>住房和城乡建设局</h5>
            <p>住房政策、城市建设规划</p>
          </div>
          <span class="policy-arrow">→</span>
        </a>
        <a href="http://jyj.putian.gov.cn/" target="_blank" class="policy-card" @click.prevent="openPolicyLink('http://jyj.putian.gov.cn/', '教育局')">
          <div class="policy-icon">🎓</div>
          <div class="policy-info">
            <h5>教育局</h5>
            <p>教育政策、学校信息、招生考试</p>
          </div>
          <span class="policy-arrow">→</span>
        </a>
        <a href="http://wjw.putian.gov.cn/" target="_blank" class="policy-card" @click.prevent="openPolicyLink('http://wjw.putian.gov.cn/', '卫健委')">
          <div class="policy-icon">🏥</div>
          <div class="policy-info">
            <h5>卫生健康委员会</h5>
            <p>医疗卫生政策、健康莆田</p>
          </div>
          <span class="policy-arrow">→</span>
        </a>
        <a href="http://jtj.putian.gov.cn/" target="_blank" class="policy-card" @click.prevent="openPolicyLink('http://jtj.putian.gov.cn/', '交通局')">
          <div class="policy-icon">🚌</div>
          <div class="policy-info">
            <h5>交通运输局</h5>
            <p>交通规划、公共交通信息</p>
          </div>
          <span class="policy-arrow">→</span>
        </a>
      </div>
    </section>

    <!-- 页脚 -->
    <footer class="landing-footer">
      <p>© 2026 莆田市市情WebGIS系统 | 课程设计项目</p>
      <p class="footer-links">
        <router-link to="/home">进入系统</router-link>
        <span>|</span>
        <a href="https://www.putian.gov.cn/" target="_blank">官方网站</a>
      </p>
    </footer>

    <!-- 政策链接弹窗 -->
    <el-dialog v-model="policyDialogVisible" :title="currentPolicyTitle" width="90%" top="5vh" class="policy-dialog">
      <div class="policy-iframe-container">
        <iframe :src="currentPolicyUrl" frameborder="0" class="policy-iframe"></iframe>
      </div>
      <template #footer>
        <el-button @click="policyDialogVisible = false">返回系统</el-button>
        <el-button type="primary" @click="openInNewTab">在新标签页打开</el-button>
      </template>
    </el-dialog>

    <!-- 城市名片详情弹窗 -->
    <el-dialog v-model="cityDetailVisible" :title="currentCityDetail.title" width="85%" top="3vh" class="city-detail-dialog" :close-on-click-modal="true">
      <div class="city-detail-content">
        <!-- 头部横幅 -->
        <div class="detail-hero">
          <img :src="currentCityDetail.heroImage" :alt="currentCityDetail.title" class="detail-hero-image" />
          <div class="detail-hero-overlay">
            <h2>{{ currentCityDetail.title }}</h2>
            <p class="detail-tagline">{{ currentCityDetail.tagline }}</p>
          </div>
        </div>
        
        <!-- 主体内容 -->
        <div class="detail-body">
          <!-- 简介 -->
          <section class="detail-section">
            <h3>📜 概述</h3>
            <p class="detail-intro">{{ currentCityDetail.intro }}</p>
          </section>
          
          <!-- 亮点卡片 -->
          <section class="detail-section">
            <h3>✨ 主要亮点</h3>
            <div class="highlights-grid">
              <div v-for="(item, idx) in currentCityDetail.highlights" :key="idx" class="highlight-card">
                <span class="highlight-icon">{{ item.icon }}</span>
                <h4>{{ item.title }}</h4>
                <p>{{ item.desc }}</p>
              </div>
            </div>
          </section>
          
          <!-- 详细介绍 -->
          <section class="detail-section" v-if="currentCityDetail.details">
            <h3>📖 详细介绍</h3>
            <div class="detail-text" v-html="currentCityDetail.details"></div>
          </section>
          
          <!-- 相关数据 -->
          <section class="detail-section" v-if="currentCityDetail.stats">
            <h3>📊 数据一览</h3>
            <div class="stats-grid">
              <div v-for="(stat, idx) in currentCityDetail.stats" :key="idx" class="stat-card">
                <span class="stat-value">{{ stat.value }}</span>
                <span class="stat-label">{{ stat.label }}</span>
              </div>
            </div>
          </section>
        </div>
      </div>
      <template #footer>
        <el-button @click="cityDetailVisible = false">返回</el-button>
        <el-button type="primary" @click="goToRelatedPage">探索更多</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router' // Import router
import { Search } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const router = useRouter()
const policyDialogVisible = ref(false)
const currentPolicyUrl = ref('')
const currentPolicyTitle = ref('')
const searchQuery = ref('') // Search text

// 关键词映射配置
const routeMappings = [
  // 内部路由
  { keywords: ['概况', '城市', '简介', 'home'], path: '/home', label: '城市概况' },
  { keywords: ['文旅', '旅游', '文化', '妈祖', '景点'], path: '/tourism', label: '文化旅游' },
  
  // 外部政务网站映射
  { keywords: ['政府', '人民政府', '官网', 'portal'], url: 'https://www.putian.gov.cn/', label: '莆田市人民政府官网' },
  { keywords: ['公开', '政务公开', '信息', 'open'], url: 'https://www.putian.gov.cn/zwgk/', label: '政务公开平台' },
  { keywords: ['服务', '办事', '大厅', '政务服务'], url: 'https://www.putian.gov.cn/zwfw/', label: '网上办事大厅' },
  { keywords: ['住建', '住房', '建设', '房产'], url: 'http://zjj.putian.gov.cn/', label: '市住建局官网' },
  { keywords: ['教育', '学校', '考试', '招生', '学区'], url: 'http://jyj.putian.gov.cn/', label: '市教育局官网' },
  { keywords: ['卫健', '卫生', '健康', '医院', '医疗'], url: 'http://wjw.putian.gov.cn/', label: '市卫健委官网' },
  { keywords: ['交通', '运输', '路', '车', '公交'], url: 'http://jtj.putian.gov.cn/', label: '市交通局官网' },
  { keywords: ['专题', '规划', '重点'], url: 'https://www.putian.gov.cn/ztzl/fwptcyfz/', label: '专题专栏' }
]

const handleSearch = () => {
  const query = searchQuery.value.trim().toLowerCase()
  if (!query) {
    ElMessage.warning('请输入搜索内容')
    return
  }

  // 查找匹配的路由
  const target = routeMappings.find(item => 
    item.keywords.some(k => query.includes(k))
  )

  if (target) {
    ElMessage.success(`正在为您跳转至：${target.label}`)
    
    if (target.url) {
      // 外部链接，新标签页打开
      window.open(target.url, '_blank')
    } else {
      // 内部路由
      router.push(target.path)
    }
  } else {
    ElMessage.info('未找到精确匹配，为您跳转至系统首页')
    router.push('/home')
  }
}

// 导入图片
import imgMeizhou from '@/assets/city-cards/meizhou_island.jpg'
import imgGuanghua from '@/assets/city-cards/guanghua_temple.jpg'
import imgMazu from '@/assets/city-cards/mazu_culture.jpg'
import imgCity from '@/assets/city-cards/city_night.jpg'

const carouselImages = [
  { name: 'meizhou', label: '湄洲岛 · 妈祖祖庙', url: imgMeizhou },
  { name: 'guanghua', label: '南山广化寺', url: imgGuanghua },
  { name: 'mazu', label: '妈祖巡安', url: imgMazu },
  { name: 'city', label: '城市夜景', url: imgCity }
]

const openPolicyLink = (url, title) => {
  currentPolicyUrl.value = url
  currentPolicyTitle.value = title
  policyDialogVisible.value = true
}

const openInNewTab = () => {
  window.open(currentPolicyUrl.value, '_blank')
}

// 城市名片详情逻辑
const cityDetailVisible = ref(false)
const currentCityDetail = ref({})

const cityDetails = {
  mazu: {
    title: '妈祖故里 · 湄洲岛',
    tagline: '立德 · 行善 · 大爱 — 世界妈祖文化中心',
    heroImage: '/images/cards/妈祖故里.jpg',
    intro: '湄洲岛是妈祖文化的发源地，也是全球5000多座妈祖庙的祖庙所在地。妈祖信俗被列入联合国人类非物质文化遗产代表作名录，是全世界华人的精神纽带。这里不仅有庄严神圣的朝圣文化，更有"南国蓬莱"之称的秀丽海岛风光。',
    highlights: [
      { title: '千年祖庙', desc: '始建于宋代，是世界上第一座妈祖庙，也是全球妈祖信众的朝圣中心。', icon: '🏯' },
      { title: '非遗信俗', desc: '妈祖祭典与黄帝陵祭典、祭孔大典并称为"中华三大祭典"。', icon: '🏮' },
      { title: '海岛风光', desc: '拥有"天下第一滩"九宝澜黄金沙滩和奇特的鹅尾神石园。', icon: '🏖️' },
      { title: '两岸纽带', desc: '每年吸引数十万台胞跨海进香，是海峡两岸交流的前沿基地。', icon: '🤝' }
    ],
    details: `<p>妈祖，原名林默，北宋建隆元年（960年）诞生于湄洲岛。她一生扶危济困、救助海难，被后世尊为"海上女神"。历代朝廷敕封达36次，从"夫人"、"妃"、"天妃"直至"天后"、"天上圣母"。</p>
              <p>如今，妈祖分灵庙遍布全球49个国家和地区，信众达3亿多人。每年农历三月二十三妈祖诞辰日和九月初九升天日，湄洲岛都会举行盛大的祭祀大典，呈现"万众朝圣"的壮观景象。</p>`,
    stats: [
      { label: '距今历史', value: '1060+ 年' },
      { label: '全球信众', value: '3亿+' },
      { label: '分灵庙宇', value: '5000+ 座' },
      { label: '国家级非遗', value: '首批' }
    ],
    relatedPath: '/tourism'
  },
  jinshi: {
    title: '文献名邦 · 进士之乡',
    tagline: '地瘦栽松柏，家贫子读书 — 千年科举奇迹',
    heroImage: '/images/cards/culture.png',
    intro: '莆田素有"海滨邹鲁"、"文献名邦"之美誉。自唐以来，这里文风鼎盛，科甲冠八闽。"家贫子读书"的祖训世代相传，创造了中国科举史上的"莆田奇迹"。',
    highlights: [
      { title: '科甲鼎盛', desc: '历史上共涌现出2482位进士、21位状元、17位宰相公卿。', icon: '📜' },
      { title: '魁元同出', desc: '宋神宗熙宁九年，文状元徐铎、武状元薛奕同出莆田，皇帝御赐诗赞。', icon: '🏆' },
      { title: '六部尚书', desc: '明代出现"六部尚书占五部"的官场奇观，足见人才之盛。', icon: '🏛️' },
      { title: '家学渊源', desc: '形成了以"方、林、黄、郑"为代表的名门望族家学传统。', icon: '📖' }
    ],
    details: `<p>莆田的科举成就于宋代达到顶峰。两宋期间，莆田（兴化军）考取进士1000多人，约占全省四分之一。王安石曾感叹："兴化多进士"。</p>
              <p>最具代表性的是"一门九进士"、"六世五状元"等家族佳话。这种重教兴学的传统一直延续至今，现代莆田依然是著名的"院士之乡"，涌现出多位两院院士。</p>`,
    stats: [
      { label: '历代进士', value: '2482 位' },
      { label: '历代状元', value: '21 位' },
      { label: '宰相公卿', value: '17 位' },
      { label: '院士专家', value: '15+ 位' }
    ],
    relatedPath: '/home'
  },
  industry: {
    title: '产业名城 · 匠心智造',
    tagline: '中国鞋都 · 工艺美术之都 — 传统与现代的交响',
    heroImage: '/images/cards/产业名城.jpg',
    intro: '莆田通过"匠心智造"实现了产业的华丽转身。这里是世界闻名的"中国鞋都"，也是精美绝伦的工艺美术之乡。如今，12条重点产业链正在重塑这座城市的经济版图。',
    highlights: [
      { title: '中国鞋都', desc: '年产鞋超16亿双，产值超千亿，全球每10双运动鞋就有1双产自这里。', icon: '👟' },
      { title: '工艺美术', desc: '木雕、金银首饰、古典家具闻名遐迩，"精微透雕"技艺独步天下。', icon: '💎' },
      { title: '平台经济', desc: '拥有国家级跨境电商综合试验区，数字经济蓬勃发展。', icon: '🌐' },
      { title: '高端装备', desc: '电子信息、新型材料等高新技术产业正在快速崛起。', icon: '⚙️' }
    ],
    details: `<p>莆田鞋业起步于上世纪80年代，经过40年发展，已形成完整的产业链条。近年来，莆田正在全力打造"莆田鞋"集体商标，推动从"代工"向"品牌"转型。</p>
              <p>同时，莆田也是中国银饰之乡和古典家具之都。仙游县的红木家具占据全国家具高端市场的半壁江山，是"仙作"流派的发源地。</p>`,
    stats: [
      { label: '鞋业产值', value: '1400+ 亿' },
      { label: '工艺产值', value: '750+ 亿' },
      { label: '年产鞋量', value: '16亿 双' },
      { label: '重点产业链', value: '12 条' }
    ],
    relatedPath: '/economy'
  },
  ecology: {
    title: '生态宜居 · 荔林水乡',
    tagline: '变害为利 · 造福人民 — 木兰溪治理的生态样本',
    heroImage: '/images/cards/生态宜居.jpeg',
    intro: '莆田依山面海，也是著名的"荔城"。这里成功实践了习近平总书记亲自擘画的木兰溪治理工程，将昔日"水患之河"变成了如今的"最美家乡河"，绘就了一幅人与自然和谐共生的美丽画卷。',
    highlights: [
      { title: '木兰溪治理', desc: '全国生态文明建设的生动范本，获评"全国十大最美家乡河"。', icon: '🌊' },
      { title: '城市绿心', desc: '拥有世界上最大的城市中心绿心——65平方公里的荔枝林带。', icon: '🌳' },
      { title: '空气优质', desc: '空气质量优良率常年保持在97%以上，稳居全省前列。', icon: '🍃' },
      { title: '人居环境', desc: '荣获主要"国家园林城市"、"国家森林城市"等称号。', icon: '🏡' }
    ],
    details: `<p>木兰溪是福建省"五江一溪"之一。自1999年启动综合治理以来，历经20年接续奋斗，全面实现了"变害为利、造福人民"的目标。现在的木兰溪两岸，已成为集防洪、生态、景观、文化于一体的带状公园。</p>
              <p>莆田城市建设保留了独特的"荔林水乡"风貌，"城在林中，水在城中"是这座城市的真实写照。</p>`,
    stats: [
      { label: '绿心面积', value: '65 km²' },
      { label: '森林覆盖率', value: '60%+' },
      { label: '空气优良率', value: '97.8%' },
      { label: '治理时长', value: '25 年' }
    ],
    relatedPath: '/environment'
  }
}

const openCityDetail = (key) => {
  if (cityDetails[key]) {
    currentCityDetail.value = cityDetails[key]
    cityDetailVisible.value = true
  }
}

const goToRelatedPage = () => {
  cityDetailVisible.value = false
  if (currentCityDetail.value.relatedPath) {
    router.push(currentCityDetail.value.relatedPath)
  }
}
</script>

<style scoped>
/* 
   Premium Light Theme (Qyer Style + Visual Polish)
*/
.landing-view {
  min-height: 100vh;
  /* Palette */
  --bg-main: #f5f9fa;        /* Cooler light gray */
  --text-primary: #2c3e50;
  --text-secondary: #5e6d82;
  --primary-color: #00b8a9;  /* Fresh Cyan-Green */
  --accent-color: #ff5a5f;   /* Coral Red */
  
  --card-shadow: 0 10px 30px rgba(0,0,0,0.05);
  --card-shadow-hover: 0 20px 40px rgba(0,0,0,0.12);
  
  /* Subtle Topo Pattern Background */
  background-color: var(--bg-main);
  background-image: url('/images/bg_texture.png');
  background-repeat: repeat;
  background-size: 600px; /* Slightly larger pattern */
  /* Removed blend mode to ensure visibility */
  
  font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
  overflow-y: auto;
}

/* Header - Floating Glass */
.landing-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 40px;
  background: rgba(255, 255, 255, 0.7); /* More transparent */
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(0,0,0,0.05);
  position: sticky;
  top: 0;
  z-index: 1000;
  transition: all 0.3s ease;
}

.logo-area {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  font-size: 32px;
}

.logo-text h1 {
  font-size: 22px;
  font-weight: 700;
  color: #2c3e50;
  letter-spacing: 0.5px;
  margin: 0;
}

.tagline {
  font-size: 12px;
  color: var(--primary-color);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.nav-btn {
  padding: 10px 28px;
  border-radius: 50px; /* Pillow shape */
  font-size: 15px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s;
}

.nav-btn.primary {
  background: linear-gradient(135deg, #ff5a5f, #ff333d);
  color: white;
  box-shadow: 0 4px 15px rgba(255, 90, 95, 0.4);
}

.nav-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 90, 95, 0.6);
}

/* System Nav (Colorful Icons) */
.system-nav {
  padding: 80px 80px;
  /* Parallax Abstract Wave Background */
  background: url('/images/nav_bg.png?v=2') no-repeat center center;
  background-size: cover;
  background-attachment: fixed;
  position: relative;
}

/* Overlay to ensure text readability on image bg */
.system-nav::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.4); /* Much lower opacity to show image */
  backdrop-filter: blur(3px); /* blur slightly */
  z-index: 0;
}

.nav-grid {
  position: relative; /* Above overlay */
  z-index: 1;
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 30px;
  max-width: 1300px;
  margin: 0 auto;
}

/* Hero Section */
.hero-section {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center; /* Center content */
  min-height: 600px;
  padding: 0 20px;
  
  background-image: linear-gradient(to bottom, rgba(44, 62, 80, 0.3), rgba(44, 62, 80, 0.1)), url('/images/hero_banner.png');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  color: white;
  text-align: center; /* Center text align */
}

.hero-content {
  z-index: 2;
  max-width: 900px;
  display: flex; /* Stack items */
  flex-direction: column;
  align-items: center;
}

.hero-title {
  margin-bottom: 24px;
}

.title-line {
  display: block;
  font-size: 64px;
  font-weight: 900;
  line-height: 1.1;
  text-shadow: 0 10px 30px rgba(0,0,0,0.3);
  letter-spacing: -2px;
}

.title-line.accent {
  background: linear-gradient(to right, #ffffff, #e0e0e0);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-desc {
  font-size: 20px;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.95);
  margin-bottom: 40px;
  max-width: 700px;
  font-weight: 400;
  text-shadow: 0 2px 8px rgba(0,0,0,0.5);
}

/* Enhanced Search Bar */
.hero-search-bar {
  display: flex;
  background: rgba(255, 255, 255, 0.95);
  padding: 6px;
  border-radius: 100px; /* Pill shape */
  width: 100%;
  max-width: 680px;
  box-shadow: 0 15px 40px rgba(0,0,0,0.3);
  backdrop-filter: blur(10px);
  margin-bottom: 60px; /* Space before stats */
  transition: transform 0.3s;
}

.hero-search-bar:focus-within {
  transform: scale(1.02);
  box-shadow: 0 20px 50px rgba(0,0,0,0.4);
}

.search-input {
  flex: 1;
  border: none;
  background: transparent;
  padding: 0 30px;
  font-size: 18px;
  outline: none;
  color: #2c3e50;
  font-weight: 500;
}

.search-input::placeholder {
  color: #999;
}

.search-btn-icon {
  background: var(--primary-color);
  color: white;
  width: 56px;
  height: 56px;
  border-radius: 50%; /* Circle button */
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 24px;
  transition: all 0.3s ease;
  margin-left: 10px;
}

.search-btn-icon:hover {
  background: #00a093;
  transform: rotate(15deg);
}

/* Stats Glass Pane */
.hero-stats {
  display: flex;
  gap: 60px;
  background: rgba(0, 0, 0, 0.3);
  padding: 20px 50px;
  border-radius: 20px;
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255,255,255,0.1);
}

.stat-item {
  text-align: center;
}

.stat-num {
  display: block;
  font-size: 42px;
  font-weight: 700;
  color: #ffdf40; /* Bright gold */
  line-height: 1;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.9);
  letter-spacing: 1px;
}

/* Image Widget (Rotated Floating) */
.hero-image {
  position: absolute;
  right: 5%;
  top: 55%;
  width: 300px;
  z-index: 10;
  display: none; /* Hide for centered layout unless on very wide screens */
}

@media (min-width: 1600px) {
  .hero-image { display: block; }
}

.image-placeholder {
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 30px 60px rgba(0,0,0,0.5);
  border: 4px solid rgba(255,255,255,0.3);
  transform: rotate(-5deg);
  transition: transform 0.5s;
}

.image-placeholder:hover {
  transform: rotate(0deg) scale(1.05);
}

.image-placeholder img {
  width: 100%;
  height: 300px;
  object-fit: cover;
}

.carousel-caption {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 8px 16px;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  font-size: 14px;
  font-weight: 500;
  text-align: center;
}

/* Sections */
.section-title {
  font-size: 32px;
  font-weight: 800;
  color: #2c3e50;
  margin-bottom: 16px;
  text-align: center;
  position: relative;
  display: inline-block;
  width: 100%;
  letter-spacing: -0.5px;
}

.section-title::after {
  content: '';
  display: block;
  width: 60px;
  height: 4px;
  background: var(--primary-color);
  margin: 16px auto 0;
  border-radius: 2px;
}

.section-desc {
  text-align: center;
  color: var(--text-secondary);
  margin-bottom: 50px;
  font-size: 16px;
}

/* City Intro */
.city-intro {
  padding: 100px 80px 80px; /* Extra top padding for hero overlap */
  background: transparent; /* Show global topo pattern */
}

.intro-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 30px;
  max-width: 1300px;
  margin: 0 auto;
}

.intro-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  text-align: center;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  border: none;
  box-shadow: var(--card-shadow);
}

.intro-card:hover {
  transform: translateY(-10px);
  box-shadow: var(--card-shadow-hover);
}

.card-image-wrapper {
  width: 100%;
  height: 220px; /* Taller images */
  overflow: hidden;
}

.card-image-wrapper img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.intro-card:hover .card-image-wrapper img {
  transform: scale(1.08); 
}

.card-content {
  padding: 28px;
  text-align: left;
}

.intro-card h4 {
  font-size: 20px;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 10px;
}

.intro-card p {
  font-size: 14px;
  line-height: 1.6;
  color: #666;
  text-align: justify;
}

/* System Nav (Colorful Icons) */
.system-nav {
  padding: 80px 80px;
  background: #f8fbff; /* Very subtle blue tint */
}

.nav-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 30px;
  max-width: 1300px;
  margin: 0 auto;
}

.nav-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 40px 20px;
  background: white;
  border-radius: 20px;
  border: 1px solid white;
  box-shadow: 0 4px 20px rgba(0,0,0,0.03);
  text-decoration: none;
  transition: all 0.3s;
}

.nav-card:hover {
  transform: translateY(-8px);
  background: white;
  box-shadow: 0 15px 30px rgba(0,0,0,0.08); /* Stronger shadow */
}

/* Colorful Icon Backgrounds - Using nth-child targets based on grid order */
.nav-card:nth-child(1) .nav-icon { background: linear-gradient(135deg, #FF6B6B, #EE5253); color: white; }
.nav-card:nth-child(2) .nav-icon { background: linear-gradient(135deg, #FDCB6E, #E17055); color: white; }
.nav-card:nth-child(3) .nav-icon { background: linear-gradient(135deg, #74B9FF, #0984E3); color: white; }
.nav-card:nth-child(4) .nav-icon { background: linear-gradient(135deg, #55EFC4, #00B894); color: white; }
.nav-card:nth-child(5) .nav-icon { background: linear-gradient(135deg, #A29BFE, #6C5CE7); color: white; }
.nav-card:nth-child(6) .nav-icon { background: linear-gradient(135deg, #81ECEC, #00CEC9); color: white; }

.nav-icon {
  width: 80px;
  height: 80px;
  border-radius: 24px;
  font-size: 36px; /* Bigger Icon */
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
  margin-bottom: 10px;
  transition: transform 0.3s;
}

.nav-card:hover .nav-icon {
  transform: scale(1.1) rotate(5deg);
}

.nav-card span {
  font-size: 16px;
  font-weight: 600;
  color: #2d3436;
}

/* Policy Section */
.policy-section {
  padding: 80px 80px;
  background: transparent; /* Show global topo pattern */
}

.policy-grid {
  gap: 20px;
}

.policy-card {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 24px;
  background: #fdfdfd;
  border: 1px solid #eee;
  border-radius: 16px;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: none;
}

.policy-card:hover {
  transform: translateY(-5px);
  border-color: var(--primary-color);
  background: white;
  box-shadow: 0 10px 25px rgba(0,0,0,0.06);
}

.policy-icon {
  font-size: 36px;
  opacity: 1;
  color: var(--primary-color);
  filter: drop-shadow(0 4px 6px rgba(0,0,0,0.05));
}

.policy-info {
  flex: 1;
}

.policy-info h5 {
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 6px;
}

.policy-info p {
  font-size: 13px;
  color: #95a5a6;
}

.policy-arrow {
  color: #dfe6e9;
  font-size: 20px;
  transition: all 0.3s;
}

.policy-card:hover .policy-arrow {
  color: var(--primary-color);
  transform: translateX(6px);
}

/* Footer */
.landing-footer {
  padding: 60px 40px;
  text-align: center;
  border-top: none;
  background: #2d3436; /* Dark footer */
  color: #b2bec3;
}

.landing-footer p {
  color: #636e72;
  margin-bottom: 12px;
}

.footer-links a {
  color: #dfe6e9;
  font-weight: 500;
  text-decoration: none;
  transition: color 0.3s;
}

.footer-links a:hover {
  color: var(--primary-color);
}

.footer-links span {
  margin: 0 12px;
  color: #636e72;
}

/* Policy Dialog */
.policy-dialog :deep(.el-dialog__body) {
  padding: 0;
}

.policy-iframe-container {
  height: 70vh;
}

.policy-iframe {
  width: 100%;
  height: 100%;
}

/* Responsive */
@media (max-width: 1200px) {
  .hero-image { display: none; } 
  .intro-cards { grid-template-columns: repeat(2, 1fr); }
  .nav-grid { grid-template-columns: repeat(3, 1fr); }
  .policy-grid { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 768px) {
  .hero-section { min-height: auto; padding: 60px 20px; flex-direction: column; }
  .title-line { font-size: 42px; }
  
  .intro-cards { grid-template-columns: 1fr; }
  .nav-grid { grid-template-columns: repeat(2, 1fr); }
  .policy-grid { grid-template-columns: 1fr; }
  
  .hero-search-bar { width: 100%; }
}

/* City Card Styles */
.clickable-card {
  cursor: pointer;
  position: relative;
  transition: all 0.3s ease;
}

.clickable-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0,0,0,0.15);
}

.card-explore-hint {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  text-align: center;
  font-size: 12px;
  color: white;
  background: rgba(0, 184, 169, 0.9);
  padding: 4px 0;
  transform: translateY(100%);
  transition: transform 0.3s ease;
  border-bottom-left-radius: 12px;
  border-bottom-right-radius: 12px;
}

.clickable-card:hover .card-explore-hint {
  transform: translateY(0);
}

.intro-card {
  overflow: hidden; /* For hint reveal */
}

/* Detail Modal Styles */
.city-detail-dialog :deep(.el-dialog__body) {
  padding: 0;
}

.city-detail-dialog :deep(.el-dialog__header) {
  display: none; /* Custom header in hero */
}

.city-detail-content {
  overflow-y: auto;
  max-height: 70vh;
}

.detail-hero {
  position: relative;
  height: 300px;
  overflow: hidden;
}

.detail-hero-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.detail-hero-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  padding: 30px;
  background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
  color: white;
}

.detail-hero-overlay h2 {
  font-size: 32px;
  margin: 0 0 8px 0;
  text-shadow: 0 2px 4px rgba(0,0,0,0.5);
}

.detail-tagline {
  font-size: 16px;
  opacity: 0.9;
  letter-spacing: 1px;
}

.detail-body {
  padding: 30px;
}

.detail-section {
  margin-bottom: 30px;
}

.detail-section h3 {
  font-size: 18px;
  color: #2c3e50;
  border-left: 4px solid var(--primary-color);
  padding-left: 10px;
  margin-bottom: 15px;
}

.detail-intro {
  font-size: 15px;
  line-height: 1.8;
  color: #5e6d82;
}

.highlights-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
}

.highlight-card {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.highlight-icon {
  font-size: 24px;
  margin-bottom: 5px;
}

.highlight-card h4 {
  font-size: 14px;
  color: #2c3e50;
  margin: 0;
}

.highlight-card p {
  font-size: 12px;
  color: #888;
  margin: 0;
  line-height: 1.4;
}

.detail-text :deep(p) {
  margin-bottom: 10px;
  line-height: 1.7;
  color: #4a4a4a;
  text-indent: 2em;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 15px;
}

.stat-card {
  text-align: center;
  padding: 15px;
  background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
  border-radius: 8px;
  border: 1px solid #eee;
}

.stat-value {
  display: block;
  font-size: 18px;
  font-weight: bold;
  color: var(--primary-color);
  margin-bottom: 5px;
}

.stat-label {
  font-size: 12px;
  color: #666;
}
</style>
