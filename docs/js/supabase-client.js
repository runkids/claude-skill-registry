/**
 * Supabase Client for Claude Skills Registry
 * 社区功能：点赞、评论、收藏同步
 */

const SUPABASE_URL = 'https://gyrtkwwnghfwesvdiwap.supabase.co';
const SUPABASE_ANON_KEY = 'sb_publishable_gAuZcQ3joPqZAnmjdMBckg_WC4DL4Sl';

// 初始化 Supabase 客户端
const supabaseClient = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// 获取或生成设备ID（匿名用户标识）
function getDeviceId() {
    let deviceId = localStorage.getItem('deviceId');
    if (!deviceId) {
        deviceId = 'device_' + crypto.randomUUID();
        localStorage.setItem('deviceId', deviceId);
    }
    return deviceId;
}

const DEVICE_ID = getDeviceId();

// ═══════════════════════════════════════════════════════════
// 点赞功能
// ═══════════════════════════════════════════════════════════

/**
 * 切换点赞状态
 * @param {string} skillInstall - 技能安装路径
 * @returns {Promise<{liked: boolean, count: number}>}
 */
async function toggleLike(skillInstall) {
    try {
        const { data, error } = await supabaseClient
            .rpc('toggle_like', {
                p_skill_install: skillInstall,
                p_device_id: DEVICE_ID
            });

        if (error) throw error;
        return data;
    } catch (error) {
        console.error('Error toggling like:', error);
        // 降级到本地存储
        return toggleLikeLocal(skillInstall);
    }
}

// 本地点赞降级方案
function toggleLikeLocal(skillInstall) {
    const likes = JSON.parse(localStorage.getItem('localLikes') || '{}');
    const isLiked = !likes[skillInstall];

    if (isLiked) {
        likes[skillInstall] = true;
    } else {
        delete likes[skillInstall];
    }

    localStorage.setItem('localLikes', JSON.stringify(likes));
    return { liked: isLiked, count: 0 };
}

/**
 * 检查是否已点赞
 * @param {string} skillInstall
 * @returns {Promise<boolean>}
 */
async function isLiked(skillInstall) {
    try {
        const { data, error } = await supabaseClient
            .from('skill_likes')
            .select('id')
            .eq('skill_install', skillInstall)
            .eq('device_id', DEVICE_ID)
            .single();

        if (error && error.code !== 'PGRST116') throw error;
        return !!data;
    } catch (error) {
        // 降级检查本地
        const likes = JSON.parse(localStorage.getItem('localLikes') || '{}');
        return !!likes[skillInstall];
    }
}

/**
 * 获取点赞数
 * @param {string} skillInstall
 * @returns {Promise<number>}
 */
async function getLikesCount(skillInstall) {
    try {
        const { data, error } = await supabaseClient
            .from('skill_stats')
            .select('likes_count')
            .eq('skill_install', skillInstall)
            .single();

        if (error && error.code !== 'PGRST116') throw error;
        return data?.likes_count || 0;
    } catch (error) {
        return 0;
    }
}

// ═══════════════════════════════════════════════════════════
// 评论功能
// ═══════════════════════════════════════════════════════════

/**
 * 添加评论
 * @param {string} skillInstall
 * @param {string} content
 * @param {string} nickname
 * @param {number} rating - 1-5
 * @returns {Promise<{id: string, success: boolean}>}
 */
async function addComment(skillInstall, content, nickname = 'Anonymous', rating = null) {
    try {
        const { data, error } = await supabaseClient
            .rpc('add_comment', {
                p_skill_install: skillInstall,
                p_device_id: DEVICE_ID,
                p_content: content,
                p_nickname: nickname,
                p_rating: rating
            });

        if (error) throw error;
        return data;
    } catch (error) {
        console.error('Error adding comment:', error);
        return { success: false, error: error.message };
    }
}

/**
 * 获取技能评论
 * @param {string} skillInstall
 * @param {number} limit
 * @param {number} offset
 * @returns {Promise<Array>}
 */
async function getComments(skillInstall, limit = 20, offset = 0) {
    try {
        const { data, error } = await supabaseClient
            .from('skill_comments')
            .select('*')
            .eq('skill_install', skillInstall)
            .eq('is_deleted', false)
            .order('created_at', { ascending: false })
            .range(offset, offset + limit - 1);

        if (error) throw error;
        return data || [];
    } catch (error) {
        console.error('Error fetching comments:', error);
        return [];
    }
}

/**
 * 删除自己的评论
 * @param {string} commentId
 * @returns {Promise<boolean>}
 */
async function deleteComment(commentId) {
    try {
        const { error } = await supabaseClient
            .from('skill_comments')
            .update({ is_deleted: true })
            .eq('id', commentId)
            .eq('device_id', DEVICE_ID);

        if (error) throw error;
        return true;
    } catch (error) {
        console.error('Error deleting comment:', error);
        return false;
    }
}

// ═══════════════════════════════════════════════════════════
// 收藏功能（云同步）
// ═══════════════════════════════════════════════════════════

/**
 * 切换收藏状态
 * @param {string} skillInstall
 * @returns {Promise<boolean>} - 新的收藏状态
 */
async function toggleFavoriteCloud(skillInstall) {
    try {
        // 检查是否已收藏
        const { data: existing } = await supabaseClient
            .from('user_favorites')
            .select('id')
            .eq('skill_install', skillInstall)
            .eq('device_id', DEVICE_ID)
            .single();

        if (existing) {
            // 取消收藏
            const { error } = await supabaseClient
                .from('user_favorites')
                .delete()
                .eq('id', existing.id);

            if (error) throw error;
            return false;
        } else {
            // 添加收藏
            const { error } = await supabaseClient
                .from('user_favorites')
                .insert({
                    skill_install: skillInstall,
                    device_id: DEVICE_ID
                });

            if (error) throw error;
            return true;
        }
    } catch (error) {
        console.error('Error toggling favorite:', error);
        // 降级到本地存储
        return toggleFavoriteLocal(skillInstall);
    }
}

// 本地收藏降级
function toggleFavoriteLocal(skillInstall) {
    const favorites = JSON.parse(localStorage.getItem('skillFavorites') || '[]');
    const index = favorites.indexOf(skillInstall);

    if (index > -1) {
        favorites.splice(index, 1);
        localStorage.setItem('skillFavorites', JSON.stringify(favorites));
        return false;
    } else {
        favorites.push(skillInstall);
        localStorage.setItem('skillFavorites', JSON.stringify(favorites));
        return true;
    }
}

/**
 * 获取所有收藏
 * @returns {Promise<Array<string>>}
 */
async function getFavorites() {
    try {
        const { data, error } = await supabaseClient
            .from('user_favorites')
            .select('skill_install')
            .eq('device_id', DEVICE_ID);

        if (error) throw error;
        return (data || []).map(f => f.skill_install);
    } catch (error) {
        // 降级到本地
        return JSON.parse(localStorage.getItem('skillFavorites') || '[]');
    }
}

/**
 * 同步本地收藏到云端
 */
async function syncFavoritesToCloud() {
    const localFavorites = JSON.parse(localStorage.getItem('skillFavorites') || '[]');
    if (localFavorites.length === 0) return;

    try {
        // 获取云端收藏
        const cloudFavorites = await getFavorites();

        // 找出需要同步的
        const toSync = localFavorites.filter(f => !cloudFavorites.includes(f));

        if (toSync.length > 0) {
            const { error } = await supabaseClient
                .from('user_favorites')
                .upsert(
                    toSync.map(skill_install => ({
                        skill_install,
                        device_id: DEVICE_ID
                    })),
                    { onConflict: 'skill_install,device_id' }
                );

            if (error) throw error;
            console.log(`Synced ${toSync.length} favorites to cloud`);
        }
    } catch (error) {
        console.error('Error syncing favorites:', error);
    }
}

// ═══════════════════════════════════════════════════════════
// 统计和排行
// ═══════════════════════════════════════════════════════════

/**
 * 获取技能统计
 * @param {string} skillInstall
 * @returns {Promise<{likes_count, comments_count, liked, favorited}>}
 */
async function getSkillStats(skillInstall) {
    try {
        const { data, error } = await supabaseClient
            .rpc('get_skill_stats', {
                p_skill_install: skillInstall,
                p_device_id: DEVICE_ID
            });

        if (error) throw error;
        return data;
    } catch (error) {
        return {
            likes_count: 0,
            comments_count: 0,
            liked: false,
            favorited: false
        };
    }
}

/**
 * 获取热门技能排行
 * @param {number} limit
 * @returns {Promise<Array>}
 */
async function getTrendingSkills(limit = 50) {
    try {
        const { data, error } = await supabaseClient
            .rpc('get_trending_skills', { p_limit: limit });

        if (error) throw error;
        return data || [];
    } catch (error) {
        console.error('Error fetching trending:', error);
        return [];
    }
}

/**
 * 批量获取多个技能的统计
 * @param {Array<string>} skillInstalls
 * @returns {Promise<Object>} - { skillInstall: { likes_count, ... } }
 */
async function getBatchStats(skillInstalls) {
    try {
        const { data, error } = await supabaseClient
            .from('skill_stats')
            .select('*')
            .in('skill_install', skillInstalls);

        if (error) throw error;

        const stats = {};
        (data || []).forEach(s => {
            stats[s.skill_install] = s;
        });
        return stats;
    } catch (error) {
        return {};
    }
}

// ═══════════════════════════════════════════════════════════
// 初始化
// ═══════════════════════════════════════════════════════════

// 页面加载时同步收藏
document.addEventListener('DOMContentLoaded', () => {
    // 延迟同步，不阻塞页面加载
    setTimeout(syncFavoritesToCloud, 2000);
});

// 导出给全局使用
window.SkillsDB = {
    toggleLike,
    isLiked,
    getLikesCount,
    addComment,
    getComments,
    deleteComment,
    toggleFavorite: toggleFavoriteCloud,
    getFavorites,
    getSkillStats,
    getTrendingSkills,
    getBatchStats,
    DEVICE_ID
};
