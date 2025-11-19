import React, { useState, useEffect } from 'react';
import { postAPI, engagementAPI, Post } from '../services/api';
import PostCard from '../components/PostCard';
import Modal from '../components/Modal';
import '../styles/FeedPage.css';

const FeedPage: React.FC = () => {
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newPost, setNewPost] = useState({ title: '', description: '', category: '', image: '' });

  useEffect(() => {
    fetchPosts();
  }, []);

  const fetchPosts = async () => {
    try {
      setLoading(true);
      const response = await postAPI.listPosts();
      setPosts(response.data.results || response.data);
    } catch (err: any) {
      setError('Failed to load posts');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreatePost = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      await postAPI.createPost(newPost);
      setNewPost({ title: '', description: '', category: '', image: '' });
      setShowCreateModal(false);
      fetchPosts();
    } catch (err: any) {
      setError('Failed to create post');
      console.error(err);
    }
  };

  const handleLikePost = async (postId: number) => {
    try {
      await engagementAPI.likePost(postId);
      fetchPosts();
    } catch (err: any) {
      console.error('Failed to like post:', err);
    }
  };

  const handleDeletePost = async (postId: number) => {
    if (confirm('Are you sure you want to delete this post?')) {
      try {
        await postAPI.deletePost(postId);
        fetchPosts();
      } catch (err: any) {
        setError('Failed to delete post');
        console.error(err);
      }
    }
  };

  return (
    <div className="feed-page">
      <div className="container">
        {error && <div className="error">{error}</div>}

        {/* Create Post Section */}
        <div className="create-post-section">
          <button className="btn btn-primary" onClick={() => setShowCreateModal(true)}>
            + Create New Post
          </button>
        </div>

        {/* Posts List */}
        {loading ? (
          <div className="loading">
            <div className="loading-spinner"></div>
          </div>
        ) : posts.length === 0 ? (
          <div className="empty-state">
            <p>No posts yet. Be the first to share your achievement!</p>
          </div>
        ) : (
          <div className="posts-grid">
            {posts.map((post) => (
              <PostCard
                key={post.id}
                post={post}
                onLike={() => handleLikePost(post.id)}
                onDelete={() => handleDeletePost(post.id)}
              />
            ))}
          </div>
        )}
      </div>

      {/* Create Post Modal */}
      {showCreateModal && (
        <Modal
          title="Create New Post"
          onClose={() => setShowCreateModal(false)}
        >
          <form onSubmit={handleCreatePost} className="modal-form">
            <div className="form-group">
              <label htmlFor="title">Title</label>
              <input
                type="text"
                id="title"
                value={newPost.title}
                onChange={(e) => setNewPost({ ...newPost, title: e.target.value })}
                placeholder="Achievement title"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="description">Description</label>
              <textarea
                id="description"
                value={newPost.description}
                onChange={(e) => setNewPost({ ...newPost, description: e.target.value })}
                placeholder="Tell your story..."
                required
              ></textarea>
            </div>

            <div className="form-group">
              <label htmlFor="category">Category</label>
              <select
                id="category"
                value={newPost.category}
                onChange={(e) => setNewPost({ ...newPost, category: e.target.value })}
              >
                <option value="">Select a category</option>
                <option value="academics">Academics</option>
                <option value="sports">Sports</option>
                <option value="music">Music</option>
                <option value="dance">Dance</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="image">Image URL</label>
              <input
                type="url"
                id="image"
                value={newPost.image}
                onChange={(e) => setNewPost({ ...newPost, image: e.target.value })}
                placeholder="https://example.com/image.jpg"
              />
            </div>

            <div style={{ display: 'flex', gap: '10px' }}>
              <button type="button" className="btn btn-outline" onClick={() => setShowCreateModal(false)}>
                Cancel
              </button>
              <button type="submit" className="btn btn-primary">
                Post
              </button>
            </div>
          </form>
        </Modal>
      )}
    </div>
  );
};

export default FeedPage;
