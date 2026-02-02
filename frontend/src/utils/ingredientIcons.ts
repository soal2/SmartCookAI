// frontend/src/utils/ingredientIcons.ts
export function getIngredientIcon(name?: string, category?: string): string {
  const n = (name || '').toLowerCase().trim().replace(/[^a-z0-9\u4e00-\u9fff\s]/gi, '');

  if (n.includes('鸡蛋') || n.includes('蛋')) return '🥚';
  if (n.includes('西红柿') || n.includes('番茄')) return '🍅';
  if (n.includes('黄瓜')) return '🥒';
  if (n.includes('胡萝卜')) return '🥕';
  if (n.includes('菠菜')) return '🥬';
  if (n.includes('大米')) return '🍚';
  if (n.includes('土豆') || n.includes('马铃薯')) return '🥔';
  if (n.includes('肥牛')) return '🥩';
  if (n.includes('酱油') || n.includes('葱')) return '🧂';
  if (n.includes('生菜') || n.includes('生菜叶')) return '🥬';
  if (n.includes('牛奶') || n.includes('奶')) return '🥛';
  if (n.includes('鸡肉')) return '🍗';
  if (category === '水果') return '🍎';
  if (category === '蔬菜') return '🥬';

  // 默认图标
  return '🥬';
}