import React from 'react';

interface PostCardProps {
    title: string;
    content: string;
    author: string;
    date: string;
    likes: number;
    comments: number;
}

const PostCard: React.FC<PostCardProps> = ({ title, content, author, date, likes, comments }) => {
    return (
        <div className="post-card">
            <h2>{title}</h2>
            <p>{content}</p>
            <p>Posted by: {author} on {date}</p>
            <div className="post-card-footer">
                <span>{likes} Likes</span>
                <span>{comments} Comments</span>
            </div>
        </div>
    );
};

export default PostCard;