<template>
  <div>
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
        <h1 class="text-2xl font-bold mb-4 sm:mb-0">Training Courses</h1>
        <!-- Search Bar -->
        <div class="relative w-full sm:w-72">
            <FeatherIcon name="search" class="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input 
                v-model="searchQuery" 
                type="text" 
                placeholder="Search courses..." 
                class="w-full pl-9 pr-4 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent text-sm" 
            />
        </div>
    </div>
    
    <!-- Loading state -->
    <div v-if="courses.loading" class="text-gray-500">Loading courses...</div>

    <!-- The 'Cards' Grid -->
    <div v-else-if="filteredCourses && filteredCourses.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div 
          v-for="course in filteredCourses" 
          :key="course.name"
          class="bg-white rounded-lg shadow-sm border p-5 cursor-pointer hover:shadow-md transition duration-200"
          @click="$router.push(`/training-courses/${course.name}`)"
        >
            <h3 class="font-bold text-lg text-gray-900 mb-1">{{ course.course_name || course.module_name }}</h3>
            <p class="text-sm text-gray-500 mb-4 line-clamp-2">
              {{ course.course_description || 'No description available.' }}
            </p>
            
            <div class="flex items-center text-xs text-gray-400 mt-auto border-t pt-3">
               <FeatherIcon name="calendar" class="w-3 h-3 mr-1" />
               <span v-if="course.start_date">{{ course.start_date }}</span>
               <span v-else>Date TBA</span>
               
               <div class="ml-auto flex items-center bg-blue-50 text-blue-600 px-2 py-1 rounded">
                 <FeatherIcon name="video" class="w-3 h-3 mr-1" />
                 {{ course.teaching_mode || 'Online' }}
               </div>
            </div>
        </div>
    </div>
    
    <!-- Empty State -->
    <div v-else class="text-gray-500 text-center py-10">
      <span v-if="searchQuery">No training courses match your search.</span>
      <span v-else>No training courses found.</span>
    </div>
  </div>
</template>

<script setup>
import { createResource } from 'frappe-ui'
import { ref, computed } from 'vue'

// Fetches ONLY the courses the user has permission to see (Teacher or Student)
// Fetches ONLY the courses the user has permission to see (Teacher or Student)
const courses = createResource({
  url: 'lms_custom.api.get_my_training_courses',
  auto: true
})

const searchQuery = ref('')

const filteredCourses = computed(() => {
    if (!courses.data) return []
    if (!searchQuery.value) return courses.data
    
    const query = searchQuery.value.toLowerCase()
    return courses.data.filter(course => {
        const title = course.course_name || course.module_name || ''
        return title.toLowerCase().includes(query)
    })
})
</script>
