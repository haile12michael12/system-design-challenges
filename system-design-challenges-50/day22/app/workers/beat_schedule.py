from celery.schedules import crontab

# Celery Beat schedule for periodic tasks
beat_schedule = {
    # Regenerate user feeds every 5 minutes
    'regenerate-user-feeds': {
        'task': 'app.workers.tasks.feed_tasks.regenerate_user_feeds',
        'schedule': crontab(minute='*/5'),
    },
    
    # Update trending posts every hour
    'update-trending-posts': {
        'task': 'app.workers.tasks.feed_tasks.update_trending_posts',
        'schedule': crontab(minute=0, hour='*'),
    },
    
    # Send daily email digests at 9 AM
    'send-daily-email-digest': {
        'task': 'app.workers.tasks.email_tasks.send_daily_digest',
        'schedule': crontab(minute=0, hour=9),
    },
    
    # Generate hourly rollups
    'generate-hourly-rollups': {
        'task': 'app.workers.tasks.rollup_tasks.generate_hourly_rollups',
        'schedule': crontab(minute=0, hour='*'),
    },
    
    # Generate daily rollups at midnight
    'generate-daily-rollups': {
        'task': 'app.workers.tasks.rollup_tasks.generate_daily_rollups',
        'schedule': crontab(minute=0, hour=0),
    },
    
    # Cleanup old cache entries daily
    'cleanup-old-cache': {
        'task': 'app.workers.tasks.feed_tasks.cleanup_old_cache',
        'schedule': crontab(minute=30, hour=2),
    },
}