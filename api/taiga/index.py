from dotenv import load_dotenv
load_dotenv()
from flask import Blueprint, jsonify, request
from taiga import TaigaAPI
import os

bp = Blueprint('taiga', __name__)

try:
    user=os.environ.get('USER')
    passw=os.environ.get('PASS')
    taiga = TaigaAPI()

    taiga.auth(
        username=user,
        password=passw
    )
except:
    pass

# User Story Endpoints
@bp.route('/userstories', methods=['GET'])
def get_user_stories():
    user_stories = taiga.user_stories.list()
    return jsonify([user_story.to_dict() for user_story in user_stories])


@bp.route('/userstories', methods=['POST'])
def create_user_story():
    user_story_data = request.get_json()
    user_story = taiga.user_stories.create(project_id=user_story_data['project_id'], subject=user_story_data['subject'])
    return jsonify(user_story.to_dict())


@bp.route('/userstories/<int:user_story_id>', methods=['GET'])
def get_user_story(user_story_id):
    user_story = taiga.user_stories.get(user_story_id)
    if user_story:
        return jsonify(user_story.to_dict())
    return jsonify({'message': 'User story not found'})


@bp.route('/userstories/<int:user_story_id>', methods=['PUT'])
def update_user_story(user_story_id):
    user_story_data = request.get_json()
    user_story = taiga.user_stories.get(user_story_id)
    if user_story:
        user_story.subject = user_story_data['subject']
        user_story.save()
        return jsonify(user_story.to_dict())
    return jsonify({'message': 'User story not found'})


@bp.route('/userstories/<int:user_story_id>', methods=['DELETE'])
def delete_user_story(user_story_id):
    user_story = taiga.user_stories.get(user_story_id)
    if user_story:
        user_story.delete()
        return jsonify({'message': 'User story deleted'})
    return jsonify({'message': 'User story not found'})


# Task Endpoints
@bp.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = taiga.tasks.list()
    return jsonify([task.to_dict() for task in tasks])


@bp.route('/tasks', methods=['POST'])
def create_task():
    task_data = request.get_json()
    task = taiga.tasks.create(user_story_id=task_data['user_story_id'], subject=task_data['subject'])
    return jsonify(task.to_dict())


@bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = taiga.tasks.get(task_id)
    if task:
        return jsonify(task.to_dict())
    return jsonify({'message': 'Task not found'})


@bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task_data = request.get_json()
    task = taiga.tasks.get(task_id)
    if task:
        task.subject = task_data['subject']
        task.save()
        return jsonify(task.to_dict())
    return jsonify({'message': 'Task not found'})


@bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = taiga.tasks.get(task_id)
    if task:
        task.delete()
        return jsonify({'message': 'Task deleted'})
    return jsonify({'message': 'Task not found'})


# Comment Endpoints
@bp.route('/comments', methods=['GET'])
def get_comments():
    comments = taiga.comments.list()
    return jsonify([comment.to_dict() for comment in comments])


@bp.route('/comments', methods=['POST'])
def create_comment():
    comment_data = request.get_json()
    comment = taiga.comments.create(object_id=comment_data['object_id'], object_type=comment_data['object_type'], content=comment_data['content'])
    return jsonify(comment.to_dict())


@bp.route('/comments/<int:comment_id>', methods=['GET'])
def get_comment(comment_id):
    comment = taiga.comments.get(comment_id)
    if comment:
        return jsonify(comment.to_dict())
    return jsonify({'message': 'Comment not found'})


@bp.route('/comments/<int:comment_id>', methods=['PUT'])
def update_comment(comment_id):
    comment_data = request.get_json()
    comment = taiga.comments.get(comment_id)
    if comment:
        comment.content = comment_data['content']
        comment.save()
        return jsonify(comment.to_dict())
    return jsonify({'message': 'Comment not found'})


@bp.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    comment = taiga.comments.get(comment_id)
    if comment:
        comment.delete()
        return jsonify({'message': 'Comment deleted'})
    return jsonify({'message': 'Comment not found'})