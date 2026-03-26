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
        <div class="bg-gray-100 rounded px-3 py-1 flex items-center text-sm font-medium" v-if="course.doc.end_date">
          <FeatherIcon name="calendar" class="w-4 h-4 mr-2" />
          Ends: {{ course.doc.end_date }}
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

    <!-- TABS NAVIGATION -->
    <div class="flex border-b mb-6 overflow-x-auto">
        <button 
            v-for="tab in tabs" :key="tab"
            @click="activeTab = tab"
            :class="[
                'px-5 py-3 font-medium text-sm border-b-2 whitespace-nowrap outline-none transition-colors border-b-2',
                activeTab === tab ? 'border-gray-900 text-gray-900' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            ]"
        >
            {{ tab }}
        </button>
    </div>

    <!-- MAIN TAB -->
    <div v-show="activeTab === 'Main'">
        <div class="bg-white rounded-lg shadow-sm border p-6 mb-6">
             <h3 class="font-bold text-xl mb-4 border-b pb-2">Module Info</h3>
             <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <p class="mb-2"><strong>Module Name:</strong> {{ course.doc.module_name || 'N/A' }}</p>
                <p class="mb-2"><strong>Created By:</strong> {{ course.doc.created_by || 'N/A' }}</p>
                <p class="mb-2"><strong>Year:</strong> {{ course.doc.year || 'N/A' }}</p>
                <p class="mb-2"><strong>Month:</strong> {{ course.doc.month || 'N/A' }}</p>
             </div>
        </div>
        <div v-html="renderDynamicTable(course.doc.lms_df, 'Choose Course', 'No course chosen.')"></div>
        <div v-html="renderDynamicTable(course.doc.module_chapters, 'Module Chapters', 'No module chapters found.')"></div>
    </div>

    <!-- DETAILS TAB -->
    <div v-show="activeTab === 'Details'">
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
                <p class="text-sm mt-2 text-red-600" v-if="course.doc.sync_error"><strong>Sync Error:</strong> {{ course.doc.sync_error }}</p>
             </div>
             <div class="mt-4 border-t pt-4" v-if="course.doc.google_classroom_id || course.doc.calendar_event_id">
                <p class="text-sm text-gray-500 mb-1" v-if="course.doc.google_classroom_id">Classroom ID: <span class="font-mono text-gray-900">{{ course.doc.google_classroom_id }}</span></p>
                <p class="text-sm text-gray-500" v-if="course.doc.calendar_event_id">Calendar Event ID: <span class="font-mono text-gray-900">{{ course.doc.calendar_event_id }}</span></p>
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

        <div v-html="renderDynamicTable(course.doc.course_sessions, 'Training Sessions', 'No sessions scheduled.')"></div>
        <div v-html="renderDynamicTable(course.doc.student_emails, 'Enrolled Students', 'No students enrolled.')"></div>
    </div>

    <!-- ATTENDANCE TAB -->
    <div v-show="activeTab === 'Attendance'">
        <div v-html="renderDynamicTable(course.doc.attendance_details, 'Attendance Details', 'No attendance details found.')"></div>
    </div>

    <!-- ASSESSMENT TAB -->
    <div v-show="activeTab === 'Assessment'">
        <div v-html="renderDynamicTable(course.doc.table_fciz, 'Assessment Details', 'No assessments found.')"></div>
    </div>

    <!-- BATCH TAB -->
    <div v-show="activeTab === 'Batch'">
        <div v-html="renderDynamicTable(course.doc.table_monf, 'Batch Details', 'No batches found.')"></div>
    </div>

    <!-- NOTES TAB -->
    <div v-show="activeTab === 'Notes'">
        <div v-html="renderDynamicTable(course.doc.lms_notes, 'LMS Notes', 'No LMS notes found.')"></div>
        <div class="bg-white rounded-lg shadow-sm border p-6 mb-6" v-if="course.doc.notes">
             <h3 class="font-bold text-xl mb-4 border-b pb-2">Notes</h3>
             <div class="text-gray-600 prose max-w-none" v-html="course.doc.notes"></div>
        </div>
        <div v-if="(!course.doc.lms_notes || course.doc.lms_notes.length === 0) && !course.doc.notes" class="bg-white rounded-lg shadow-sm border p-6 mb-6 text-center text-gray-500 italic">No notes found.</div>
    </div>

    <!-- FEEDBACK TAB -->
    <div v-show="activeTab === 'Feedback'">
        <div class="bg-white rounded-lg shadow-sm border p-6 mb-6">
             <h3 class="font-bold text-xl mb-4 border-b pb-2">Feedback</h3>
              <div v-if="course.doc.feed_back_1" class="mb-4">
                  <p class="font-bold text-gray-700 text-sm mb-1">Feedback 1:</p>
                  <div class="text-gray-600 bg-gray-50 p-4 rounded">{{ course.doc.feed_back_1 }}</div>
              </div>
              <div v-if="course.doc.feed_back_2" class="mb-4">
                  <p class="font-bold text-gray-700 text-sm mb-1">Feedback 2:</p>
                  <div class="text-gray-600 bg-gray-50 p-4 rounded">{{ course.doc.feed_back_2 }}</div>
              </div>
              <p v-if="!course.doc.feed_back_1 && !course.doc.feed_back_2" class="text-gray-500 italic">No feedback registered.</p>
        </div>
    </div>

    <!-- ASSIGNMENT TAB -->
    <div v-show="activeTab === 'Assignment'">
        <div class="bg-white rounded-lg shadow-sm border p-6 mb-6">
             <h3 class="font-bold text-xl mb-4 border-b pb-2">Assignment</h3>
             <div v-if="course.doc.route">
                 <p class="mb-2"><strong>Route:</strong> {{ course.doc.route }}</p>
             </div>
             <p v-else class="text-gray-500 italic">No assignment details available.</p>
        </div>
    </div>

  </div>
  
  <!-- Loading state -->
  <div v-else class="py-10 text-center text-gray-500">Loading course details...</div>
</template>

<script setup>
import { createDocumentResource } from 'frappe-ui'
import { useRoute } from 'vue-router'
import { ref } from 'vue'

const route = useRoute()

const tabs = ['Main', 'Details', 'Attendance', 'Assessment', 'Batch', 'Notes', 'Feedback', 'Assignment']
const activeTab = ref('Details')

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

// Universal function to parse any Frappe Child Table dynamically without knowing its fields
const renderDynamicTable = (tableData, title, emptyMessage) => {
    if (!tableData || tableData.length === 0) {
        return `<div class="bg-white rounded-lg shadow-sm border p-6 mb-6 text-center text-gray-500">${emptyMessage}</div>`;
    }

    const unneededFields = ['name', 'owner', 'creation', 'modified', 'modified_by', 'docstatus', 'idx', 'parent', 'parentfield', 'parenttype', '_user_tags', '_comments', '_assign', '_liked_by'];
    const allKeys = Object.keys(tableData[0]);
    const columns = allKeys.filter(k => !unneededFields.includes(k));

    if (columns.length === 0) return '';

    const formatLabel = (str) => {
        return str.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
    };

    let thead = `<tr class="bg-gray-50 text-gray-600 text-sm border-b">`;
    columns.forEach(col => {
        thead += `<th class="p-3 font-medium whitespace-nowrap text-left">${formatLabel(col)}</th>`;
    });
    thead += `</tr>`;

    let tbody = '';
    tableData.forEach(row => {
        tbody += `<tr class="border-b last:border-0 hover:bg-gray-50">`;
        columns.forEach(col => {
            let val = row[col];
            if (val === null || val === undefined) val = '';
            // Make file paths clickable
            if (typeof val === 'string' && (val.startsWith('/files/') || val.startsWith('/private/files/'))) {
                const fileName = val.split('/').pop();
                tbody += `<td class="p-3 text-sm"><a href="${val}" target="_blank" class="text-blue-600 hover:text-blue-800 underline">${fileName}</a></td>`;
            } else if (typeof val === 'string' && (val.startsWith('http://') || val.startsWith('https://'))) {
                tbody += `<td class="p-3 text-sm"><a href="${val}" target="_blank" class="text-blue-600 hover:text-blue-800 underline">${val}</a></td>`;
            } else {
                tbody += `<td class="p-3 text-sm">${val}</td>`;
            }
        });
        tbody += `</tr>`;
    });

    return `
        <div class="bg-white rounded-lg shadow-sm border p-6 mb-6">
             <h3 class="font-bold text-xl mb-4 border-b pb-2">${title}</h3>
             <div class="overflow-x-auto">
                 <table class="w-full text-left border-collapse">
                     <thead>${thead}</thead>
                     <tbody>${tbody}</tbody>
                 </table>
             </div>
        </div>
    `;
};

// Automatically fetches the specific document based on the URL parameter
const course = createDocumentResource({
  doctype: 'Training Course', // Your exact Doctpye Name
  name: route.params.name, // The ID taken from the URL
  auto: true
})
</script>
