<template>
  <div>
    <h1 class="text-2xl font-bold mb-6">Training Courses</h1>
    
    <!-- Loading state -->
    <div v-if="courses.list.loading" class="text-gray-500">Loading courses...</div>

    <!-- The 'Cards' Grid -->
    <div v-else-if="courses.data && courses.data.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div 
          v-for="course in courses.data" 
          :key="course.name"
          class="bg-white rounded-lg shadow-sm border p-5 cursor-pointer hover:shadow-md transition duration-200"
          @click="$router.push(`/training-courses/${course.route || course.name}`)"
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
      No training courses found.
    </div>
  </div>
</template>

<script setup>
import { createListResource } from 'frappe-ui'

// Automatically fetches the records from your ERPNext backend
const courses = createListResource({
  doctype: 'Training Course', // Your exact Doctpye Name
  // Ask the backend to return these specific fields from your list
  fields: [
    'name', 'module_name', 'course_name', 'course_description', 
    'start_date', 'teaching_mode', 'route'
  ],
  limit: 100,
  auto: true
})
</script>
