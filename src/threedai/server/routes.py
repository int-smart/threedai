from flask import request, jsonify, send_file
import os
import uuid
import tempfile

def register_routes(app, model):
    @app.route('/api/process', methods=['POST'])
    def process_image():
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
            
        image_file = request.files['image']
        
        # Generate unique ID for this process
        process_id = str(uuid.uuid4())
        
        # Process the image with the model
        video_path, model3d_path = model.process_image(image_file, process_id)
        
        return jsonify({
            'process_id': process_id,
            'video_url': f'/api/results/{process_id}/video',
            'model3d_url': f'/api/results/{process_id}/model3d'
        })
    
    @app.route('/api/results/<process_id>/video')
    def get_video(process_id):
        video_path = model.get_video_path(process_id)
        if os.path.exists(video_path):
            return send_file(video_path, mimetype='video/mp4')
        return jsonify({'error': 'Video not found'}), 404
        
    @app.route('/api/results/<process_id>/model3d')
    def get_model3d(process_id):
        model3d_path = model.get_model3d_path(process_id)
        if os.path.exists(model3d_path):
            return send_file(model3d_path, mimetype='application/octet-stream',
                            as_attachment=True, attachment_filename=f'model_{process_id}.step')
        return jsonify({'error': '3D model not found'}), 404
        
    @app.route('/')
    def index():
        return app.send_static_file('index.html')
