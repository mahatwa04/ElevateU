import React from 'react';
import { Post } from '../services/api';
import '../styles/PostCard.css';

interface PostCardProps {
  post: Post;
  onLike: () => void;
  onDelete: () => void;
}

const PostCard: React.FC<PostCardProps> = ({ post, onLike, onDelete }) => {
  return (
    <div className="post-card">
      {post.image && <img src={post.image} alt={post.title} className="post-image" />}

      <div className="post-header">
        <div className="post-meta">
          <h3>{post.title}</h3>
          <p className="post-author">By {post.user.username}</p>
        </div>
        {post.category && <span className="post-badge">{post.category}</span>}
      </div>

      <p className="post-description">{post.description}</p>

      <div className="post-stats">
        <span className="stat">❤️ {post.like_count} Likes</span>
        <span className="stat">💬 {post.comment_count} Comments</span>
      </div>

      <div className="post-actions">
        <button className="btn-action" onClick={onLike} title="Like">
          ❤️ Like
        </button>
        <button className="btn-action" title="Comment">
          💬 Comment
        </button>
        <button className="btn-action btn-danger" onClick={onDelete} title="Delete">
          🗑️ Delete
        </button>
      </div>

      <small className="post-date">{new Date(post.created_at).toLocaleDateString()}</small>
    </div>
  );
};

export default PostCard;
