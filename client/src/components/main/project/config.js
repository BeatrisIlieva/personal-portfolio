export const mediaConfig = {
    'add-to-bag':
        'Validates size selection on both client and server sides - prevents cart addition and shows error message when users attempt to add items without selecting a size.',
    'product-list':
        'Filters automatically recalculate after each selection to show only valid combinations and products count based on available inventory.',
    register:
        'Extended Django User model with email as primary identifier and custom authentication backend supporting email/username login. \n\n JWT authentication, automatic profile creation, and welcome email via Celery with Redis Cloud. \n\n Registration form with custom password validators and instant field validation using regex patterns before form submission preventing invalid requests to backend.',
    'product-review':
        'Product review functionality restricted to authenticated users who have purchased the item. Includes admin moderation system where Order group users can manage customer feedback.',
    'reset-password':
        'Two-phase password reset: email submission generates token and base64-encoded UID sent via email link. \n\n  Reset confirmation validates token authenticity, enforces password requirements using Django validators, and triggers success notification through asynchronous email processing.'
};
