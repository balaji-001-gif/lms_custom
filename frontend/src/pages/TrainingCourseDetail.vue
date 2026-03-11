<template>
  <div v-if="course.doc">
    <!-- Back Button -->
    <button @click="$router.push('/training-courses')" class="flex items-center text-gray-500 hover:text-gray-800 mb-6 text-sm">
      <FeatherIcon name="arrow-left" class="w-4 h-4 mr-1" /> Back to Courses
    </button>
    
    <!-- Header Section -->
    <div class="bg-white rounded-lg shadow-sm border p-6 mb-6">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">{{ course.doc.course_name || course.doc.module_name }}</h1>
      <p class="text-gray-600 text-lg whitespace-pre-line" v-if="course.doc.course_description">{{ course.doc.course_description }}</p>
      
      <div class="flex flex-wrap gap-4 mt-6">
        <div class="bg-gray-100 rounded px-3 py-1 flex items-center text-sm font-medium" v-if="course.doc.start_time && course.doc.class_to">
          <FeatherIcon name="clock" class="w-4 h-4 mr-2" />
          {{ formatTime(course.doc.start_time) }} - {{ formatTime(course.doc.class_to) }} ({{ course.doc.duration }} Mins)
        </div>
        <div class="bg-gray-100 rounded px-3 py-1 flex items-center text-sm font-medium" v-if="course.doc.start_date">
          <FeatherIcon name="calendar" class="w-4 h-4 mr-2" />
          Starts: {{ course.doc.start_date }}
        </div>
        <div class="bg-gray-100 rounded px-3 py-1 flex items-center text-sm font-medium" v-if="course.doc.room">
          <FeatherIcon name="map-pin" class="w-4 h-4 mr-2" />
          Room: {{ course.doc.room }}
        </div>
         <div class="bg-gray-100 rounded px-3 py-1 flex items-center text-sm font-medium" v-if="course.doc.classroom_code">
          <FeatherIcon name="hash" class="w-4 h-4 mr-2" />
          Code: {{ course.doc.classroom_code }}
        </div>
      </div>
    </div>

    <!-- Integrations & Details Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
      <!-- Session Info -->
      <div class="bg-white rounded-lg shadow-sm border p-6">
         <h3 class="font-bold text-xl mb-4 border-b pb-2">Class Details</h3>
         <p class="mb-2"><strong>Lecturer:</strong> {{ course.doc.teacher_email || course.doc.link_doej || 'Not assigned' }}</p>
         <p class="mb-2"><strong>Teaching Mode:</strong> {{ course.doc.teaching_mode || 'N/A' }}</p>
         <p class="mb-2"><strong>Total Classes:</strong> {{ course.doc.total_no_of_class || 0 }}</p>
         <p class="mb-2" v-if="course.doc.class_days"><strong>Days:</strong> {{ course.doc.class_days }}</p>
         <div class="mb-2" v-if="getDaysChecked(course.doc)">
            <strong>Weekly Schedule:</strong> {{ getDaysChecked(course.doc) }}
         </div>
         <p class="mb-2" v-if="course.doc.section"><strong>Section:</strong> {{ course.doc.section }}</p>
         <p class="mb-2" v-if="course.doc.company"><strong>Company:</strong> {{ course.doc.company }}</p>
      </div>

      <!-- Google Classrom Links -->
      <div class="bg-white rounded-lg shadow-sm border p-6">
         <h3 class="font-bold text-xl mb-4 border-b pb-2">Integrations & Links</h3>
         
         <div v-if="course.doc.google_classroom_link || course.doc.google_meet_link">
             <a :href="course.doc.google_classroom_link" target="_blank" class="block w-full text-center bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-4 rounded mb-3 transition" v-if="course.doc.google_classroom_link">
               Open Google Classroom
             </a>
             
             <a :href="course.doc.google_meet_link" target="_blank" class="block w-full text-center bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded transition" v-if="course.doc.google_meet_link">
               Join Google Meet
             </a>
             <p class="mt-4 text-sm text-gray-500" v-if="course.doc.enrollment_code">Enrollment Code: <span class="font-mono text-gray-900">{{ course.doc.enrollment_code }}</span></p>
         </div>
         <div v-else>
            <p class="text-gray-500 italic">No links available</p>
         </div>
         
         <div class="mt-4 border-t pt-4" v-if="course.doc.sync_status">
            <p class="text-sm"><strong>Sync Status:</strong> <span class="px-2 py-0.5 rounded text-xs" :class="course.doc.sync_status === 'Success' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'">{{ course.doc.sync_status }}</span></p>
         </div>
      </div>
    </div>

    <!-- Exam Details -->
    <div class="bg-white rounded-lg shadow-sm border p-6 mb-6" v-if="course.doc.exam_start_date || course.doc.exam_end_date">
         <h3 class="font-bold text-xl mb-4 border-b pb-2">Exam Schedule</h3>
         <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
                <p class="text-sm text-gray-500">Exam Start</p>
                <p class="font-medium">{{ course.doc.exam_start_date }}</p>
            </div>
            <div>
                <p class="text-sm text-gray-500">Exam End</p>
                <p class="font-medium">{{ course.doc.exam_end_date }}</p>
            </div>
         </div>
    </div>

    <!-- Course Sessions (Child Table mapping 'course_sessions') -->
    <div class="bg-white rounded-lg shadow-sm border p-6 mb-6" v-if="course.doc.course_sessions && course.doc.course_sessions.length > 0">
         <h3 class="font-bold text-xl mb-4 border-b pb-2">Training Sessions</h3>
         <div class="overflow-x-auto">
             <table class="w-full text-left border-collapse">
                 <thead>
                     <tr class="bg-gray-50 text-gray-600 text-sm border-b">
                         <th class="p-3 font-medium">Session / Topic</th>
                         <th class="p-3 font-medium">Date</th>
                     </tr>
                 </thead>
                 <tbody>
                     <tr v-for="session in course.doc.course_sessions" :key="session.name" class="border-b last:border-0 hover:bg-gray-50">
                         <td class="p-3">{{ session.title || session.session_name || session.name || session.session }}</td>
                         <td class="p-3">{{ session.date || session.start_time || 'TBA' }}</td>
                     </tr>
                 </tbody>
             </table>
         </div>
    </div>
    
    <!-- Students (Child Table mapping 'student_emails') -->
    <div class="bg-white rounded-lg shadow-sm border p-6 mb-6" v-if="course.doc.student_emails && course.doc.student_emails.length > 0">
         <h3 class="font-bold text-xl mb-4 border-b pb-2">Enrolled Students</h3>
         <div class="overflow-x-auto">
             <table class="w-full text-left border-collapse">
                 <thead>
                     <tr class="bg-gray-50 text-gray-600 text-sm border-b">
                         <th class="p-3 font-medium">Student / Email</th>
                     </tr>
                 </thead>
                 <tbody>
                     <tr v-for="student in course.doc.student_emails" :key="student.name" class="border-b last:border-0 hover:bg-gray-50">
                         <td class="p-3">{{ student.student_email || student.student || student.email || student.name }}</td>
                     </tr>
                 </tbody>
             </table>
         </div>
    </div>

    <!-- Notes & Feedback -->
    <div class="bg-white rounded-lg shadow-sm border p-6 mb-6" v-if="course.doc.notes || course.doc.feed_back_1 || course.doc.feed_back_2">
         <h3 class="font-bold text-xl mb-4 border-b pb-2">Additional Information</h3>
         <div v-if="course.doc.notes">
             <p class="font-bold text-gray-700 text-sm mt-4 mb-1">Notes:</p>
             <p class="text-gray-600 whitespace-pre-line">{{ course.doc.notes }}</p>
         </div>
         <div v-if="course.doc.feed_back_1">
             <p class="font-bold text-gray-700 text-sm mt-4 mb-1">Feedback 1:</p>
             <p class="text-gray-600 whitespace-pre-line">{{ course.doc.feed_back_1 }}</p>
         </div>
         <div v-if="course.doc.feed_back_2">
             <p class="font-bold text-gray-700 text-sm mt-4 mb-1">Feedback 2:</p>
             <p class="text-gray-600 whitespace-pre-line">{{ course.doc.feed_back_2 }}</p>
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

const formatTime = (timeStr) => {
    if (!timeStr) return '';
    const parts = timeStr.split(':');
    if (parts.length >= 2) return `${parts[0]}:${parts[1]}`;
    return timeStr;
}

const getDaysChecked = (doc) => {
    const days = [];
    if (doc.sunday) days.push('Sunday');
    if (doc.monday) days.push('Monday');
    if (doc.tuesday) days.push('Tuesday');
    if (doc.wednesday) days.push('Wednesday');
    if (doc.thursday) days.push('Thursday');
    if (doc.friday) days.push('Friday');
    if (doc.saturday) days.push('Saturday');
    return days.join(', ');
}

// Automatically fetches the specific document based on the URL parameter
const course = createDocumentResource({
  doctype: 'Training Course', // Your exact Doctpye Name
  name: route.params.name, // The ID taken from the URL
  auto: true
})
</script>
