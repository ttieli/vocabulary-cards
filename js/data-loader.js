/**
 * VocabularyDataLoader - 模块化词汇数据加载器
 *
 * 用途：从cards-data/文件夹结构中动态加载主题和词汇数据
 *
 * 使用方法：
 * const loader = new VocabularyDataLoader();
 * const data = await loader.loadAll();
 *
 * 或者按需加载：
 * await loader.loadThemes();
 * await loader.loadThemeCards('mario');
 */

class VocabularyDataLoader {
  /**
   * 构造函数
   * @param {string} basePath - 数据文件的基础路径，默认为 './cards-data/'
   */
  constructor(basePath = './cards-data/') {
    this.basePath = basePath;
    this.config = null;
    this.themes = null;
    this.cards = {};
    this._loadCache = new Map(); // 缓存已加载的数据
    this._cacheBuster = `v=${Date.now()}`; // Cache busting parameter
  }

  /**
   * 添加缓存破坏参数到URL
   * @param {string} url - 原始URL
   * @returns {string} 带缓存破坏参数的URL
   */
  _addCacheBuster(url) {
    const separator = url.includes('?') ? '&' : '?';
    return `${url}${separator}${this._cacheBuster}`;
  }

  /**
   * 加载配置文件
   * @returns {Promise<Object>} 配置对象
   */
  async loadConfig() {
    const cacheKey = 'config';
    if (this._loadCache.has(cacheKey)) {
      return this._loadCache.get(cacheKey);
    }

    try {
      const url = this._addCacheBuster(`${this.basePath}config.json`);
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`Failed to load config: ${response.statusText}`);
      }
      this.config = await response.json();
      this._loadCache.set(cacheKey, this.config);
      return this.config;
    } catch (error) {
      console.error('Error loading config:', error);
      throw error;
    }
  }

  /**
   * 加载主题配置
   * @returns {Promise<Object>} 主题配置对象
   */
  async loadThemes() {
    const cacheKey = 'themes';
    if (this._loadCache.has(cacheKey)) {
      return this._loadCache.get(cacheKey);
    }

    try {
      const url = this._addCacheBuster(`${this.basePath}themes.json`);
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`Failed to load themes: ${response.statusText}`);
      }
      const data = await response.json();
      this.themes = data.themes;
      this._loadCache.set(cacheKey, this.themes);
      return this.themes;
    } catch (error) {
      console.error('Error loading themes:', error);
      throw error;
    }
  }

  /**
   * 加载特定主题的词汇卡片
   * @param {string} themeId - 主题ID (如 'mario', 'zelda', 'hayday')
   * @returns {Promise<Array>} 词汇卡片数组
   */
  async loadThemeCards(themeId) {
    const cacheKey = `cards_${themeId}`;
    if (this._loadCache.has(cacheKey)) {
      return this._loadCache.get(cacheKey);
    }

    try {
      const url = this._addCacheBuster(`${this.basePath}cards/${themeId}.json`);
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`Failed to load cards for theme '${themeId}': ${response.statusText}`);
      }
      const data = await response.json();
      this.cards[themeId] = data.cards || [];
      this._loadCache.set(cacheKey, this.cards[themeId]);
      return this.cards[themeId];
    } catch (error) {
      console.error(`Error loading cards for theme '${themeId}':`, error);
      throw error;
    }
  }

  /**
   * 加载所有主题的词汇卡片
   * @returns {Promise<Object>} 包含所有主题卡片的对象 {themeId: [cards]}
   */
  async loadAllCards() {
    // 确保主题已加载
    if (!this.themes) {
      await this.loadThemes();
    }

    const themeIds = Object.keys(this.themes);
    const loadPromises = themeIds.map(themeId => this.loadThemeCards(themeId));

    await Promise.all(loadPromises);
    return this.cards;
  }

  /**
   * 加载所有数据（配置、主题、所有卡片）
   * @returns {Promise<Object>} 完整的数据对象
   */
  async loadAll() {
    try {
      await this.loadConfig();
      await this.loadThemes();
      await this.loadAllCards();

      return this.getData();
    } catch (error) {
      console.error('Error loading all data:', error);
      throw error;
    }
  }

  /**
   * 获取当前已加载的数据（格式兼容旧的cards-data.json）
   * @returns {Object} 数据对象 {themes: {...}, cards: {...}}
   */
  getData() {
    return {
      themes: this.themes || {},
      cards: this.cards || {}
    };
  }

  /**
   * 清除缓存
   */
  clearCache() {
    this._loadCache.clear();
    this.config = null;
    this.themes = null;
    this.cards = {};
  }

  /**
   * 获取数据统计信息
   * @returns {Object} 统计信息
   */
  getStats() {
    const themeCount = this.themes ? Object.keys(this.themes).length : 0;
    const cardCounts = {};
    let totalCards = 0;

    for (const [themeId, cards] of Object.entries(this.cards)) {
      cardCounts[themeId] = cards.length;
      totalCards += cards.length;
    }

    return {
      themes: themeCount,
      totalCards: totalCards,
      cardsByTheme: cardCounts,
      cacheSize: this._loadCache.size
    };
  }
}

// 导出供其他模块使用
if (typeof module !== 'undefined' && module.exports) {
  module.exports = VocabularyDataLoader;
}
