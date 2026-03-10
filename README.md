# LMS Custom Vue Pages

This repository contains the required Vue 3 pages to display your Custom `Training Course` doctype gracefully inside the Frappe LMS frontend.

## Instructions to Install

Since you cannot hot-load Vue components dynamically from the backend into Frappe LMS without a complex build pipeline, you need to paste these files directly into the LMS core frontend.

**1. Copy the Vue Files**
Copy the two `.vue` files located in `frontend/src/pages/` to your server's LMS app directory:
`cd frappe-bench/apps/lms/frontend/src/pages/`
Paste them there.

**2. Update the Router**
Open `frappe-bench/apps/lms/frontend/src/router.js` (or `router/index.js`) and add the routes so the app knows about the new pages:

```javascript
{
  path: '/training-courses',
  name: 'TrainingCourseList',
  component: () => import('@/pages/TrainingCourseList.vue')
},
{
  path: '/training-courses/:name', 
  name: 'TrainingCourseDetail',
  component: () => import('@/pages/TrainingCourseDetail.vue')
}
```

**3. Update the Sidebar**
Open `frappe-bench/apps/lms/frontend/src/components/Sidebar.vue` (or similar file) and add the menu link:

```html
<router-link 
  to="/training-courses" 
  class="flex items-center rounded-md p-2 hover:bg-gray-100"
>
  <FeatherIcon name="book-open" class="h-4 w-4 mr-2" /> 
  <span>Training Courses</span>
</router-link>
```

**4. Build the Frontend**
Run this from your server terminal:
```bash
cd frappe-bench/apps/lms/frontend
yarn build
```

After the build completes, hard refresh `milms.aimaxl.com` and your new custom Course Doctypes will appear beautifully in the UI!
