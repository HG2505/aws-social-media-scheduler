import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  Calendar, 
  Clock, 
  Send, 
  Sparkles, 
  Upload, 
  Trash2, 
  CheckCircle2, 
  AlertCircle, 
  Facebook, 
  Instagram, 
  Linkedin, 
  Twitter,
  Server,
  Cloud,
  Database
} from 'lucide-react';

const API_BASE = '/api';

export default function App() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  
  // Form State
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [platform, setPlatform] = useState('FACEBOOK');
  const [scheduledAt, setScheduledAt] = useState('');
  const [mediaUrl, setMediaUrl] = useState('');
  
  // AI Modal State
  const [isAiModalOpen, setIsAiModalOpen] = useState(false);
  const [aiTopic, setAiTopic] = useState('');
  const [aiTone, setAiTone] = useState('Professional');
  const [aiLoading, setAiLoading] = useState(false);

  useEffect(() => {
    fetchPosts();
  }, []);

  const fetchPosts = async () => {
    try {
      setLoading(true);
      const res = await axios.get(`${API_BASE}/posts/`);
      setPosts(res.data);
    } catch (err) {
      console.error('Failed to fetch posts:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      setUploading(true);
      const res = await axios.post(`${API_BASE}/posts/upload-media`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setMediaUrl(res.data.media_url);
    } catch (err) {
      alert('Upload to S3 failed: ' + err.message);
    } finally {
      setUploading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!title || !content || !scheduledAt) {
      alert('Please fill out all required fields!');
      return;
    }

    try {
      await axios.post(`${API_BASE}/posts/`, {
        title,
        content,
        platform,
        scheduled_at: new Date(scheduledAt).toISOString(),
        media_url: mediaUrl || null
      });

      // Reset Form
      setTitle('');
      setContent('');
      setMediaUrl('');
      setScheduledAt('');
      fetchPosts();
    } catch (err) {
      const detail = err.response?.data?.detail;
      const errorMsg = typeof detail === 'string' 
        ? detail 
        : Array.isArray(detail) 
          ? detail.map(d => d.msg).join(', ') 
          : (err.message || 'Failed to schedule post');
      alert(errorMsg);
    }
  };

  const handlePublishNow = async (id) => {
    try {
      await axios.post(`${API_BASE}/posts/${id}/publish-now`);
      fetchPosts();
    } catch (err) {
      alert('Failed to publish now');
    }
  };

  const handleDelete = async (id) => {
    if (!confirm('Are you sure you want to cancel & delete this scheduled post?')) return;
    try {
      await axios.delete(`${API_BASE}/posts/${id}`);
      fetchPosts();
    } catch (err) {
      alert('Failed to delete post');
    }
  };

  const handleGenerateAiCaption = async () => {
    if (!aiTopic) return alert('Please enter a topic for AI');
    try {
      setAiLoading(true);
      const res = await axios.post(`${API_BASE}/ai/generate-caption`, {
        topic: aiTopic,
        tone: aiTone,
        platform: platform
      });
      
      const fullText = `${res.data.caption}\n\n${res.data.hashtags.join(' ')}`;
      setContent(fullText);
      setIsAiModalOpen(false);
    } catch (err) {
      alert('AI Generation failed');
    } finally {
      setAiLoading(false);
    }
  };

  const getPlatformIcon = (p) => {
    switch (p) {
      case 'FACEBOOK': return <Facebook class="w-4 h-4 text-blue-500" />;
      case 'INSTAGRAM': return <Instagram class="w-4 h-4 text-pink-500" />;
      case 'LINKEDIN': return <Linkedin class="w-4 h-4 text-sky-400" />;
      case 'TWITTER': return <Twitter class="w-4 h-4 text-blue-400" />;
      default: return <Facebook class="w-4 h-4 text-slate-400" />;
    }
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case 'SCHEDULED':
        return <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/20"><Clock className="w-3 h-3" /> Scheduled</span>;
      case 'PUBLISHED':
        return <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"><CheckCircle2 className="w-3 h-3" /> Published</span>;
      default:
        return <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-slate-500/10 text-slate-400 border border-slate-500/20"><AlertCircle className="w-3 h-3" /> {status}</span>;
    }
  };

  return (
    <div className="min-h-screen pb-12">
      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-950/80 backdrop-blur sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center shadow-lg shadow-cyan-500/20">
              <Calendar className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="font-bold text-lg text-slate-100 flex items-center gap-2">
                Social Post Scheduler
                <span className="text-xs px-2 py-0.5 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 font-mono">AWS EventBridge</span>
              </h1>
              <p className="text-xs text-slate-400">Automated Content Publishing Pipeline</p>
            </div>
          </div>

          {/* AWS Badges */}
          <div className="hidden md:flex items-center gap-4 text-xs">
            <div className="flex items-center gap-1.5 text-slate-400 bg-slate-900 px-3 py-1.5 rounded-lg border border-slate-800">
              <Cloud className="w-4 h-4 text-amber-500" /> S3 Storage
            </div>
            <div className="flex items-center gap-1.5 text-slate-400 bg-slate-900 px-3 py-1.5 rounded-lg border border-slate-800">
              <Server className="w-4 h-4 text-purple-400" /> EventBridge
            </div>
            <div className="flex items-center gap-1.5 text-slate-400 bg-slate-900 px-3 py-1.5 rounded-lg border border-slate-800">
              <Database className="w-4 h-4 text-blue-400" /> PostgreSQL
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 pt-8 grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Left Column: Form */}
        <div className="lg:col-span-5">
          <div className="glass-card rounded-2xl p-6 shadow-xl border border-slate-800">
            <h2 className="text-lg font-bold text-slate-100 mb-6 flex items-center gap-2">
              <Send className="w-5 h-5 text-cyan-400" /> Schedule New Post
            </h2>

            <form onSubmit={handleSubmit} className="space-y-5">
              {/* Title */}
              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">Post Title</label>
                <input
                  type="text"
                  placeholder="e.g. Product Announcement Q4"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-200 focus:outline-none focus:border-cyan-500 transition"
                  required
                />
              </div>

              {/* Platform & Date */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">Platform</label>
                  <select
                    value={platform}
                    onChange={(e) => setPlatform(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-200 focus:outline-none focus:border-cyan-500 transition"
                  >
                    <option value="FACEBOOK">Facebook</option>
                    <option value="INSTAGRAM">Instagram</option>
                    <option value="LINKEDIN">LinkedIn</option>
                    <option value="TWITTER">Twitter (X)</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">Publish Date & Time</label>
                  <input
                    type="datetime-local"
                    value={scheduledAt}
                    onChange={(e) => setScheduledAt(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-200 focus:outline-none focus:border-cyan-500 transition"
                    required
                  />
                </div>
              </div>

              {/* Content & AI Button */}
              <div>
                <div className="flex justify-between items-center mb-2">
                  <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400">Post Caption</label>
                  <button
                    type="button"
                    onClick={() => setIsAiModalOpen(true)}
                    className="inline-flex items-center gap-1.5 text-xs text-cyan-400 hover:text-cyan-300 font-semibold transition"
                  >
                    <Sparkles className="w-3.5 h-3.5" /> AI Copilot
                  </button>
                </div>
                <textarea
                  rows={4}
                  placeholder="Write your caption here or click AI Copilot to generate..."
                  value={content}
                  onChange={(e) => setContent(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-200 focus:outline-none focus:border-cyan-500 transition resize-none"
                  required
                />
              </div>

              {/* Media Upload (S3) */}
              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">Media Attachment (AWS S3)</label>
                <div className="flex items-center gap-3">
                  <label className="cursor-pointer bg-slate-950 hover:bg-slate-900 border border-slate-800 border-dashed rounded-xl px-4 py-2.5 text-xs text-slate-400 flex items-center gap-2 transition">
                    <Upload className="w-4 h-4 text-cyan-400" />
                    {uploading ? 'Uploading to S3...' : 'Upload Image'}
                    <input type="file" onChange={handleFileUpload} accept="image/*" className="hidden" />
                  </label>
                  {mediaUrl && (
                    <span className="text-xs text-emerald-400 font-medium truncate max-w-[200px]">✓ S3 Uploaded</span>
                  )}
                </div>
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                className="w-full bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white font-semibold rounded-xl py-3 text-sm shadow-lg shadow-cyan-500/25 transition active:scale-[0.99]"
              >
                Schedule Post with AWS EventBridge
              </button>
            </form>
          </div>
        </div>

        {/* Right Column: List of Posts */}
        <div className="lg:col-span-7">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
              <Calendar className="w-5 h-5 text-blue-400" /> Scheduled Posts Queue
            </h2>
            <span className="text-xs bg-slate-800 text-slate-300 font-semibold px-2.5 py-1 rounded-full">
              {posts.length} Posts
            </span>
          </div>

          {loading ? (
            <div className="text-center py-12 text-slate-500">Loading queue...</div>
          ) : posts.length === 0 ? (
            <div className="glass-card rounded-2xl p-12 text-center text-slate-400 border border-slate-800">
              <Calendar className="w-12 h-12 text-slate-600 mx-auto mb-3" />
              <p className="font-semibold text-slate-300">No scheduled posts yet</p>
              <p className="text-xs text-slate-500 mt-1">Fill in the form on the left to schedule your first post.</p>
            </div>
          ) : (
            <div className="space-y-4">
              {posts.map((post) => (
                <div key={post.id} className="glass-card rounded-2xl p-5 border border-slate-800 hover:border-slate-700 transition space-y-3">
                  <div className="flex items-start justify-between">
                    <div className="flex items-center gap-2.5">
                      <div className="p-2 bg-slate-900 rounded-lg border border-slate-800">
                        {getPlatformIcon(post.platform)}
                      </div>
                      <div>
                        <h3 className="font-bold text-sm text-slate-100">{post.title}</h3>
                        <p className="text-xs text-slate-400">
                          Scheduled: {new Date(post.scheduled_at).toLocaleString()}
                        </p>
                      </div>
                    </div>
                    {getStatusBadge(post.status)}
                  </div>

                  {/* Content Preview */}
                  <p className="text-xs text-slate-300 whitespace-pre-wrap line-clamp-3 bg-slate-950/60 p-3 rounded-xl border border-slate-900 font-mono">
                    {post.content}
                  </p>

                  {/* Actions */}
                  <div className="flex items-center justify-between pt-2 border-t border-slate-800/80 text-xs">
                    <span className="text-slate-500 font-mono text-[11px]">
                      ID: {post.eventbridge_schedule_name || post.id}
                    </span>
                    <div className="flex items-center gap-2">
                      {post.status === 'SCHEDULED' && (
                        <button
                          onClick={() => handlePublishNow(post.id)}
                          className="px-3 py-1.5 bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 font-semibold rounded-lg border border-emerald-500/20 transition"
                        >
                          Publish Now
                        </button>
                      )}
                      <button
                        onClick={() => handleDelete(post.id)}
                        className="p-1.5 text-slate-400 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition"
                        title="Delete Post"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>

      {/* AI Copilot Modal */}
      {isAiModalOpen && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="glass-card rounded-2xl p-6 max-w-md w-full border border-slate-800 shadow-2xl">
            <h3 className="text-base font-bold text-slate-100 mb-4 flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-cyan-400" /> AI Caption Generator
            </h3>

            <div className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1">Topic or Keywords</label>
                <input
                  type="text"
                  placeholder="e.g. AWS Cloud Launch, 50% Sale, New Feature"
                  value={aiTopic}
                  onChange={(e) => setAiTopic(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-200 focus:outline-none focus:border-cyan-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1">Tone of Voice</label>
                <select
                  value={aiTone}
                  onChange={(e) => setAiTone(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-200 focus:outline-none focus:border-cyan-500"
                >
                  <option value="Professional">Professional</option>
                  <option value="Casual & Friendly">Casual & Friendly</option>
                  <option value="Excited & Urgent">Excited & Urgent</option>
                  <option value="Humorous">Humorous</option>
                </select>
              </div>

              <div className="flex justify-end gap-3 pt-4">
                <button
                  type="button"
                  onClick={() => setIsAiModalOpen(false)}
                  className="px-4 py-2 text-xs text-slate-400 hover:text-slate-200 font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="button"
                  onClick={handleGenerateAiCaption}
                  disabled={aiLoading}
                  className="px-4 py-2 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold rounded-xl text-xs shadow-lg shadow-cyan-500/20"
                >
                  {aiLoading ? 'Generating...' : 'Generate Caption'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
