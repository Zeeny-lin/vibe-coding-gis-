<template>
  <div class="meizhou-view">
    <!-- Hero Section -->
    <div class="hero-section">
      <div class="hero-content">
        <h1>走进湄洲岛</h1>
        <p class="subtitle">妈祖故里 · 南国蓬莱 · 东方夏威夷</p>

      </div>
    </div>

    <!-- 导航栏 -->
    <div class="nav-bar" :class="{ 'scrolled': isScrolled }">
      <div class="nav-container">
        <router-link to="/tourism" class="back-link">← 返回旅游板块</router-link>
        <div class="nav-links">
          <a href="#overview" class="active">岛屿概况</a>
          <a href="#spots">必游景点</a>
          <a href="#culture">妈祖文化</a>
          <a href="#guide">游玩攻略</a>
        </div>
      </div>
    </div>

    <!-- 岛屿概况 -->
    <section id="overview" class="section-container">
      <div class="section-header">
        <h2>🏝️ 岛屿概况</h2>
        <p>Meizhou Island Overview</p>
      </div>
      <div class="overview-content">
        <div class="overview-text">
          <p>湄洲岛位于福建省莆田市秀屿区湄洲湾畔，素有"南国蓬莱"之美誉，是妈祖文化的发祥地，也是全球3亿多妈祖信众魂牵梦萦的"东方麦加"。全岛陆域面积14.35平方公里，海岸线蜿蜒30.4公里，拥有13处总长20公里的金色沙滩，被誉为"天下第一滩"。</p>
          <p>作为国家5A级旅游景区，湄洲岛集碧海、金沙、绿林、海岩、奇石、庙宇于一体。这里不仅有雄伟庄严的妈祖祖庙，更有鬼斧神工的鹅尾神石园和闻名遐迩的湄屿潮音。岛上气候宜人，四季如春，森林覆盖率高，是理想的滨海度假胜地与生态朝圣之所。</p>
          <p>2009年9月30日，"妈祖信俗"被联合国教科文组织列入人类非物质文化遗产代表作名录，成为中国首个信俗类世界遗产。每年农历三月廿三妈祖诞辰日和九月初九妈祖升天日，岛上都会举行盛大的祭祀大典，吸引世界各地游客与信众前来观礼祈福。</p>
        </div>
        <div class="overview-image">
          <!-- 确保图片存在 -->
          <img src="/images/cards/meizhou_main.webp" alt="湄洲岛全景" />
        </div>
      </div>
    </section>

    <!-- 必游景点 -->
    <section id="spots" class="section-container alt-bg">
      <div class="section-header">
        <h2>🏞️ 必游景点</h2>
        <p>Must-Visit Attractions</p>
      </div>
      <div class="spots-grid">
        <div class="spot-card" v-for="spot in spots" :key="spot.name">
          <div class="spot-image" :style="{ backgroundImage: `url(${spot.image})` }">
            <div class="spot-tag">{{ spot.tag }}</div>
          </div>
          <div class="spot-info">
            <h3>{{ spot.name }}</h3>
            <p>{{ spot.desc }}</p>
            <div class="spot-meta">
              <span>📍 {{ spot.location }}</span>
              <span>⭐ {{ spot.rating }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 妈祖文化 -->
    <section id="culture" class="section-container">
      <div class="section-header">
        <h2>🏮 妈祖文化</h2>
        <p>Mazu Culture</p>
      </div>
      <div class="culture-grid">
        <div class="culture-card" v-for="item in cultureItems" :key="item.title">
          <div class="culture-image" :style="{ backgroundImage: `url(${item.image})` }"></div>
          <div class="culture-content">
            <h3>{{ item.title }}</h3>
            <p>{{ item.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 游玩攻略 -->
    <section id="guide" class="section-container alt-bg">
      <div class="section-header">
        <h2>🧭 游玩攻略</h2>
        <p>Travel Guide</p>
      </div>
      <div class="guide-grid">
        <div class="guide-card">
          <div class="guide-icon">⛴️</div>
          <h3>进岛交通</h3>
          <ul>
            <li><strong>轮渡:</strong> 文甲码头 ⇄ 湄洲码头</li>
            <li><strong>时间:</strong> 7:00 - 17:40 (每20分钟一班)</li>
            <li><strong>夜航:</strong> 18:00 - 21:00 (整点发船)</li>
            <li><strong>票价:</strong> 船票+门票 通票制</li>
          </ul>
        </div>
        <div class="guide-card">
          <div class="guide-icon">🚌</div>
          <h3>岛上交通</h3>
          <ul>
            <li><strong>公交:</strong> 覆盖主要景点 (2元/人)</li>
            <li><strong>电瓶车:</strong> 随叫随停，方便快捷</li>
            <li><strong>共享单车:</strong> 环岛骑行最佳选择</li>
            <li><strong>步行:</strong> 栈道漫步，风景绝佳</li>
          </ul>
        </div>
        <div class="guide-card">
          <div class="guide-icon">📅</div>
          <h3>最佳时节</h3>
          <ul>
            <li><strong>4月-10月:</strong> 滨海游玩、踏浪戏水最佳</li>
            <li><strong>3月/9月:</strong> 农历三月廿三、九月初九看祭典</li>
            <li><strong>夏季:</strong> 这里的夏天没有酷暑</li>
            <li><strong>冬季:</strong> 感受不一样海岛风情</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- Footer CTA -->
    <div class="footer-cta">
      <h2>准备好开启您的朝圣之旅了吗？</h2>
      <a href="https://wap.lotsmall.cn/vue/detail/ticket?activityTags=&id=5187&m_id=820&refer=listPage" target="_blank" class="cta-btn">预订船票 / 了解更多</a>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const isScrolled = ref(false)

const spots = [
  {
    name: '妈祖祖庙',
    desc: '世界上第一座妈祖庙，是妈祖信仰的发源地，建筑宏伟，文化底蕴深厚。',
    location: '湄洲岛北部',
    rating: '5.0',
    tag: '5A核心',
    image: '/images/cards/mazu_temple.webp'
  },
  {
    name: '黄金沙滩',
    desc: '被誉为"天下第一滩"，沙质洁白，海天一色，是游泳和看日落的绝佳去处。',
    location: '湄洲岛西南端',
    rating: '4.8',
    tag: '休闲度假',
    image: '/images/cards/golden_beach.png'
  },
  {
    name: '鹅尾神石园',
    desc: '因形似鹅尾而得名，拥有众多奇特的海蚀地貌，是摄影爱好者的天堂。',
    location: '湄洲岛东南端',
    rating: '4.9',
    tag: '自然奇观',
    image: '/images/cards/ewei_park.webp'
  },
  {
    name: '湄屿潮音',
    desc: '莆田二十四景之一，在此可听潮音赏月，感受大自然的鬼斧神工。',
    location: '湄洲岛最北端',
    rating: '4.7',
    tag: '听涛观澜',
    image: '/images/cards/meiyu_tide.png'
  }
]

const cultureItems = [
  {
    title: '非遗信俗',
    desc: '妈祖信俗是世界非物质文化遗产，是中国首个信俗类世界遗产。每年的妈祖祭典与黄帝陵祭典、祭孔大典并称为"中华三大祭典"。',
    image: '/images/cards/mazu_heritage.webp'
  },
  {
    title: '春秋大祭',
    desc: '农历三月二十三（诞辰日）和九月初九（升天日）是岛上最盛大的日子，世界各地信众云集，举行盛大的祭祀大典。',
    image: '/images/cards/spring_autumn_sacrifice.webp'
  },
  {
    title: '朝圣习俗',
    desc: '进香团队往往手持进香旗，抬着妈祖神像，敲锣打鼓，以此表达对妈祖的虔诚和敬意。',
    image: '/images/cards/pilgrimage_customs.webp'
  }
]

const handleScroll = (e) => {
  // e.target是滚动容器
  isScrolled.value = e.target.scrollTop > 50
}

onMounted(() => {
  // 监听页面容器的滚动事件，因为它是独立的滚动区域
  const container = document.querySelector('.meizhou-view')
  if (container) {
    container.addEventListener('scroll', handleScroll)
  }
})

onUnmounted(() => {
  const container = document.querySelector('.meizhou-view')
  if (container) {
    container.removeEventListener('scroll', handleScroll)
  }
})
</script>

<style scoped>
/* Hero Section */
.meizhou-view {
  height: 100%;
  overflow-y: auto;
  scroll-behavior: smooth;
  position: relative;
  background-color: #f8faff; /* 极淡的蓝白色 */
  /* 使用细腻柔和的背景，去除突兀的纹理 */
  background-image: 
    linear-gradient(180deg, #ffffff 0%, #f0f7fa 100%);
}

.hero-section {
  height: 60vh;
  background: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.4)), url('/images/cards/meizhou_island_hero.jpg');
  background-size: cover;
  background-position: center;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: white;
  position: relative;
}

.hero-content h1 {
  font-size: 48px;
  margin-bottom: 16px;
  text-shadow: 0 2px 4px rgba(0,0,0,0.5);
}

.subtitle {
  font-size: 20px;
  opacity: 0.9;
  letter-spacing: 2px;
  margin-bottom: 40px;
}



/* Nav Bar */
.nav-bar {
  position: sticky;
  top: 0;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  z-index: 100;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  padding: 15px 0;
  transition: all 0.3s;
}

.nav-bar.scrolled {
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  padding: 10px 0;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.back-link {
  color: #666;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.back-link:hover {
  color: var(--primary-color);
}

.nav-links {
  display: flex;
  gap: 30px;
}

.nav-links a {
  color: #333;
  text-decoration: none;
  font-weight: 500;
  padding-bottom: 5px;
  border-bottom: 2px solid transparent;
}

.nav-links a:hover, .nav-links a.active {
  color: #00b8a9;
  border-bottom-color: #00b8a9;
}

/* Sections */
.section-container {
  padding: 80px 20px;
  max-width: 1200px;
  margin: 0 auto;
  scroll-margin-top: 80px;
}

.section-container.alt-bg {
  background-color: #f9f9f9;
  max-width: 100%;
}

.section-container.alt-bg > div {
  max-width: 1200px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  margin-bottom: 60px;
  position: relative;
}

.section-header h2 {
  font-size: 36px;
  color: #333;
  margin-bottom: 15px;
  display: inline-block;
  position: relative;
  font-weight: bold;
}

.section-header {
  text-align: center;
  margin-bottom: 50px;
  position: relative;
  padding-bottom: 20px;
}

.section-header h2 {
  font-size: 32px;
  color: #333;
  margin-bottom: 12px;
  display: inline-block;
  position: relative;
  font-weight: 700;
  letter-spacing: 2px;
}

/* 简约高级的标题装饰 - 底部红色短线 */
.section-header h2::after {
  content: '';
  display: block;
  width: 60px;
  height: 4px;
  background: #C41E3A;
  margin: 15px auto 0;
  border-radius: 2px;
}

.section-header p {
  color: #888;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 4px;
  font-weight: 500;
  margin-top: 15px;
}

/* Overview */
.overview-content {
  display: flex;
  gap: 50px;
  align-items: center;
}

.overview-text {
  flex: 1;
  font-size: 16px;
  line-height: 1.8;
  color: #555;
}

.overview-text p {
  margin-bottom: 20px;
}

.overview-image {
  flex: 1;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 20px 40px rgba(0,0,0,0.1);
}

.overview-image img {
  width: 100%;
  height: auto;
  display: block;
}

/* Spots */
.spots-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 30px;
}

.spot-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0,0,0,0.05);
  display: flex;
  transition: all 0.4s ease;
  border: 1px solid rgba(0,0,0,0.05);
}

.spot-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 15px 40px rgba(196, 30, 58, 0.15); /* 红韵阴影 */
  border-color: rgba(196, 30, 58, 0.2);
}

.spot-image {
  width: 200px;
  background: #eee; /* Placeholder color */
  background-image: url('/images/cards/city_night.jpg'); /* Default bg */
  background-size: cover;
  position: relative;
}

.spot-tag {
  position: absolute;
  top: 10px;
  left: 10px;
  background: rgba(0,0,0,0.6);
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.spot-info {
  flex: 1;
  padding: 25px;
}

.spot-info h3 {
  margin: 0 0 10px 0;
  color: #333;
}

.spot-info p {
  color: #666;
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 15px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.spot-meta {
  display: flex;
  gap: 15px;
  font-size: 13px;
  color: #999;
}

/* Culture */
.culture-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
}

.culture-card {
  background: #fff;
  border: 1px solid rgba(0,0,0,0.05);
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.4s ease;
  display: flex;
  flex-direction: column;
  box-shadow: 0 5px 15px rgba(0,0,0,0.03);
}

.culture-card:hover {
  border-color: #C41E3A; /* 妈祖红 */
  box-shadow: 0 15px 30px rgba(196, 30, 58, 0.15);
  transform: translateY(-8px);
}

.culture-image {
  height: 160px;
  background-size: cover;
  background-position: center;
}

.culture-content {
  padding: 25px;
  text-align: center;
}

.culture-content h3 {
  color: #333;
  margin-bottom: 15px;
  position: relative;
  display: inline-block;
}

.culture-content h3::after {
  content: '';
  display: block;
  width: 30px;
  height: 2px;
  background: #e74c3c;
  margin: 10px auto 0;
}

.culture-content p {
  color: #666;
  font-size: 14px;
  line-height: 1.6;
}

/* Guide */
.guide-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
}

.guide-card {
  background: white;
  padding: 30px;
  border-radius: 16px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.05);
  border: 1px solid transparent;
  transition: all 0.3s;
  position: relative;
  overflow: hidden;
}

.guide-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(90deg, #C41E3A, #FFD700);
  opacity: 0;
  transition: opacity 0.3s;
}

.guide-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0,0,0,0.1);
}

.guide-card:hover::before {
  opacity: 1;
}

.guide-icon {
  font-size: 32px;
  margin-bottom: 20px;
  color: #00b8a9;
}

.guide-card h3 {
  margin-bottom: 20px;
  color: #333;
}

.guide-card ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.guide-card li {
  margin-bottom: 12px;
  font-size: 14px;
  color: #666;
  display: flex;
  align-items: center;
}

.guide-card li strong {
  color: #333;
  margin-right: 8px;
  width: 70px;
}

/* Footer CTA */
.footer-cta {
  background: #333;
  color: white;
  text-align: center;
  padding: 80px 20px;
}

.footer-cta h2 {
  font-size: 32px;
  margin-bottom: 30px;
}

.cta-btn {
  display: inline-block;
  padding: 15px 40px;
  background: #00b8a9;
  color: white;
  text-decoration: none;
  border-radius: 30px;
  font-weight: bold;
  font-size: 18px;
  transition: background 0.3s;
}

.cta-btn:hover {
  background: #00a093;
}

@media (max-width: 768px) {
  .overview-content { flex-direction: column; }
  .spots-grid { grid-template-columns: 1fr; }
  .culture-grid { grid-template-columns: 1fr; }
  .guide-grid { grid-template-columns: 1fr; }

}
</style>
