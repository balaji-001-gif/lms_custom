<template>
  <div v-if="course.doc">
    <!-- Back Button -->
    <button @click="$router.push('/training-courses')" class="flex items-center text-gray-500 hover:text-gray-800 mb-6 text-sm">
      <FeatherIcon name="arrow-left" class="w-4 h-4 mr-1" /> Back to Courses
    </button>
    
    <!-- Header Section -->
    <div class="bg-white rounded-lg shadow-sm border p-6 mb-6">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">{{ course.doc.course_name || course.doc.module_name }}</h1>
      <p class="text-gray-600 text-lg">{{ course.doc.course_description }}</p>
      
      <div class="flex flex-wrap gap-4 mt-6">
        <div class="bg-gray-100 rounded px-3 py-1 flex items-center text-sm font-medium">
          <FeatherIcon name="clock" class="w-4 h-4 mr-2" />
          {{ course.doc.start_time }} - {{ course.doc.class_to }} ({{ course.doc.duration }} Mins)
        </div>
        <div class="bg-gray-100 rounded px-3 py-1 flex items-center text-sm font-medium">
          <FeatherIcon name="calendar" class="w-4 h-4 mr-2" />
          Starts: {{ course.doc.start_date }}
        </div>
        <div class="bg-gray-100 rounded px-3 py-1 flex items-center text-sm font-medium" v-if="course.doc.room">
          <FeatherIcon name="map-pin" class="w-4 h-4 mr-2" />
          Room: {{ course.doc.room }}
        </div>
      </div>
    </div>

    <!-- Integrations & Details Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- Session Info -->
      <div class="bg-white rounded-lg shadow-sm border p-6">
         <h3 class="font-bold text-xl mb-4 border-b pb-2">Class Details</h3>
         <p class="mb-2"><strong>Lecturer:</strong> {{ course.doc.teacher_email || 'Not assigned' }}</p>
         <p class="mb-2"><strong>Teaching Mode:</strong> {{ course.doc.teaching_mode }}</p>
         <p class="mb-2"><strong>Total Classes:</strong> {{ course.doc.total_no_of_class }}</p>
         <p v-if="course.doc.class_days"><strong>Days:</strong> {{ course.doc.class_days }}</p>
      </div>

      <!-- Google Classrom Links -->
      <div class="bg-white rounded-lg shadow-sm border p-6" v-if="course.doc.google_classroom_link || course.doc.google_meet_link">
         <h3 class="font-bold text-xl mb-4 border-b pb-2">Google Classroom</h3>
         
         <a :href="course.doc.google_classroom_link" target="_blank" class="block w-full text-center bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-4 rounded mb-3 transition" v-if="course.doc.google_classroom_link">
           Open Google Classroom
         </a>
         
         <a :href="course.doc.google_meet_link" target="_blank" class="block w-full text-center bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded transition" v-if="course.doc.google_meet_link">
           Join Google Meet
         </a>

         <p class="mt-4 text-sm text-gray-500">Enrollment Code: <span class="font-mono text-gray-900">{{ course.doc.enrollment_code }}</span></p>
      </div>
    </div>
  </div>
  
  <!-- Loading state -->
  <div v-else class="py-10 text-center text-gray-500">Loading course details...</div>
</template>

<script setup>
import { createDocumentResource } from 'frappe-ui'
import { useRoute } from 'vue-router'

const route = useRoute()

// Automatically fetches the specific document based on the URL parameter
const course = createDocumentResource({
  doctype: 'Training Course', // Your exact Doctpye Name
  name: route.params.name, // The ID taken from the URL
  auto: true
})
</script>
