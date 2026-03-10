import frappe
import os
import shutil
import subprocess
import re

def get_lms_frontend_path():
    try:
        lms_path = frappe.get_app_path('lms')
        return os.path.join(os.path.dirname(lms_path), 'frontend')
    except Exception:
        return None

def inject_lms_customizations(*args, **kwargs):
    print("\\n🚀 [lms_custom] Injecting Custom LMS frontend pages...\\n")
    lms_frontend_path = get_lms_frontend_path()
    
    if not lms_frontend_path or not os.path.exists(lms_frontend_path):
        print("⚠️ [lms_custom] LMS frontend not found. Skipping Vue injection.\\n")
        return

    # Find where the custom vue pages are stored
    custom_frontend_path = os.path.join(os.path.dirname(frappe.get_app_path('lms_custom')), 'frontend')
    
    # 1. Copy pages to the LMS app
    target_pages_dir = os.path.join(lms_frontend_path, 'src', 'pages')
    os.makedirs(target_pages_dir, exist_ok=True)
    
    try:
        shutil.copy(os.path.join(custom_frontend_path, 'src', 'pages', 'TrainingCourseList.vue'), os.path.join(target_pages_dir, 'TrainingCourseList.vue'))
        shutil.copy(os.path.join(custom_frontend_path, 'src', 'pages', 'TrainingCourseDetail.vue'), os.path.join(target_pages_dir, 'TrainingCourseDetail.vue'))
        print("✅ Copied Vue Pages to LMS App")
    except Exception as e:
        print(f"❌ Failed to copy Pages: {e}")
        return

    # 2. Patch router.js
    router_path = os.path.join(lms_frontend_path, 'src', 'router.js')
    if not os.path.exists(router_path):
        router_path = os.path.join(lms_frontend_path, 'src', 'router', 'index.js')

    if os.path.exists(router_path):
        with open(router_path, 'r') as f:
            router_content = f.read()

        route_injection = """
  {
    path: '/training-courses',
    name: 'TrainingCourseList',
    component: () => import('@/pages/TrainingCourseList.vue')
  },
  {
    path: '/training-courses/:name', 
    name: 'TrainingCourseDetail',
    component: () => import('@/pages/TrainingCourseDetail.vue')
  },
"""
        if "TrainingCourseList" not in router_content:
            # Insert the routes right at the top of the routes array
            router_content = router_content.replace('const routes = [', 'const routes = [\\n' + route_injection)
            router_content = router_content.replace('let routes = [', 'let routes = [\\n' + route_injection)
            
            with open(router_path, 'w') as f:
                f.write(router_content)
            print("✅ Patched Router (router.js)")
        else:
            print("✅ Router already patched")

    # 3. Patch Sidebar Element
    # Locate where the /courses link is to append our link
    components_dir = os.path.join(lms_frontend_path, 'src', 'components')
    sidebar_injection = """
        <router-link 
          to="/training-courses" 
          class="flex items-center rounded-md p-2 hover:bg-gray-100 text-gray-700 font-medium"
        >
          <FeatherIcon name="book-open" class="h-4 w-4 mr-2 text-gray-500" /> 
          <span>Training Courses</span>
        </router-link>
"""
    patched_sidebar = False
    if os.path.exists(components_dir):
        for root, dirs, files in os.walk(components_dir):
            for file in files:
                if file.endswith('.vue'):
                    filepath = os.path.join(root, file)
                    with open(filepath, 'r') as f:
                        content = f.read()
                    
                    if 'to="/courses"' in content or "to='/courses'" in content:
                        if "to=\\"/training-courses\\"" not in content and "to='/training-courses'" not in content:
                            # Use regex to inject snippet right after the closing tag of the Courses link
                            content = re.sub(r'(<router-link[^>]*to=[\'"]/courses[\'"][^>]*>.*?</router-link>)', r'\\1' + sidebar_injection, content, flags=re.DOTALL)
                            with open(filepath, 'w') as f:
                                f.write(content)
                            print(f"✅ Patched Sidebar ({file})")
                        patched_sidebar = True

    if not patched_sidebar:
        print("⚠️ Could not find LMS Sidebar to patch. Link will only be accessible via direct URL.")

    # 4. Trigger yarn build in LMS frontend
    print("⏳ Building LMS Frontend... (This may take a minute)\\n")
    try:
        subprocess.run(['yarn', 'install'], cwd=lms_frontend_path, check=False)
        subprocess.run(['yarn', 'build'], cwd=lms_frontend_path, check=False)
        print("\\n🎉 [lms_custom] Build Complete! Your custom pages are injected.\\n")
    except Exception as e:
        print(f"❌ Failed to run build: {e}")

