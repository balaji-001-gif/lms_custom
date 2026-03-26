<template>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="flex flex-col space-y-6 mb-8">
      <div class="flex items-center justify-between">
        <h1 class="text-3xl font-extrabold text-gray-900 tracking-tight">Training Courses</h1>
      </div>

      <!-- Filter Bar -->
      <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0 bg-white p-4 rounded-xl shadow-sm border border-gray-100">
        
        <!-- Status Pills -->
        <div class="flex items-center space-x-2 overflow-x-auto pb-2 lg:pb-0 scrollbar-hide">
          <button 
            v-for="status in ['All', 'Live', 'Upcoming', 'Completed']" 
            :key="status"
            @click="activeStatus = status"
            :class="[
              'px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 whitespace-nowrap',
              activeStatus === status 
                ? 'bg-gray-900 text-white shadow-md' 
                : 'bg-gray-50 text-gray-600 hover:bg-gray-100 border border-transparent'
            ]"
          >
            {{ status }}
          </button>
        </div>

        <div class="flex flex-col sm:flex-row items-center space-y-3 sm:space-y-0 sm:space-x-3">
          <!-- Search Input -->
          <div class="relative w-full sm:w-64">
            <FeatherIcon name="search" class="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input 
              v-model="searchQuery" 
              type="text" 
              placeholder="Search by Title" 
              class="w-full pl-10 pr-4 py-2 bg-gray-50 border-transparent focus:bg-white focus:ring-2 focus:ring-gray-900 focus:border-transparent rounded-lg text-sm transition-all duration-200 border border-gray-100" 
            />
          </div>

          <!-- Teaching Mode Dropdown -->
          <select 
            v-model="activeMode"
            class="w-full sm:w-48 pl-3 pr-10 py-2 bg-gray-50 border-transparent focus:bg-white focus:ring-2 focus:ring-gray-900 focus:border-transparent rounded-lg text-sm appearance-none border border-gray-100"
          >
            <option value="All">All Teaching Modes</option>
            <option value="Online">Online</option>
            <option value="Face to Face">Face to Face</option>
            <option value="Blended">Blended</option>
          </select>
        </div>
      </div>
    </div>
    
    <!-- Loading state -->
    <div v-if="courses.loading" class="text-gray-500">Loading courses...</div>

    <!-- The 'Cards' Grid -->
    <div v-else-if="filteredCourses && filteredCourses.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div 
          v-for="course in filteredCourses" 
          :key="course.name"
          class="flex flex-col bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-xl hover:-translate-y-1 transition-all duration-300 group"
          @click="$router.push(`/training-courses/${course.name}`)"
        >
            <!-- Card Header Space (Placeholder for Image/Gradient) -->
            <div class="h-40 bg-gradient-to-br from-gray-800 to-gray-900 flex items-center justify-center p-6 text-center">
               <h3 class="font-bold text-xl text-white line-clamp-2 leading-tight group-hover:scale-105 transition-transform duration-300">
                 {{ course.course_name || course.module_name }}
               </h3>
            </div>

            <div class="p-6 flex flex-col flex-grow">
               <p class="text-sm text-gray-500 mb-6 line-clamp-3 leading-relaxed">
                 {{ course.course_description || 'Master this comprehensive training module with our expert-led sessions.' }}
               </p>
               
               <div class="mt-auto pt-4 border-t border-gray-50 flex items-center justify-between">
                  <div class="flex items-center text-xs font-medium text-gray-500">
                     <FeatherIcon name="calendar" class="w-3.5 h-3.5 mr-1.5 text-gray-400" />
                     <span>{{ course.start_date || 'Date TBA' }}</span>
                  </div>
                  
                  <div 
                    :class="[
                       'flex items-center px-2.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider',
                       course.teaching_mode === 'Online' ? 'bg-blue-50 text-blue-600' : 
                       course.teaching_mode === 'Face to Face' ? 'bg-orange-50 text-orange-600' : 
                       'bg-purple-50 text-purple-600'
                    ]"
                  >
                    <FeatherIcon :name="course.teaching_mode === 'Online' ? 'video' : 'map-pin'" class="w-3 h-3 mr-1" />
                    {{ course.teaching_mode || 'Online' }}
                  </div>
               </div>
            </div>
        </div>
    </div>
    
    <!-- Empty State -->
    <div v-else class="flex flex-col items-center justify-center py-20 bg-gray-50 rounded-2xl border-2 border-dashed border-gray-200">
      <div class="bg-white p-4 rounded-full shadow-sm border mb-4">
        <FeatherIcon name="search" class="w-8 h-8 text-gray-300" />
      </div>
      <h3 class="text-lg font-bold text-gray-900 mb-1">No courses found</h3>
      <p class="text-gray-500 text-sm max-w-xs text-center">
        <span v-if="searchQuery || activeStatus !== 'All' || activeMode !== 'All'">Try adjustment your filters or checking back later for more training availability.</span>
        <span v-else>No training courses have been published yet.</span>
      </p>
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
const activeStatus = ref('All')
const activeMode = ref('All')

const filteredCourses = computed(() => {
    if (!courses.data) return []
    
    const today = new Date().toISOString().split('T')[0]
    
    return courses.data.filter(course => {
        // 1. Search Logic
        const query = searchQuery.value.toLowerCase()
        const title = (course.course_name || course.module_name || '').toLowerCase()
        const matchesSearch = !query || title.includes(query)
        
        // 2. Status Logic
        let matchesStatus = true
        if (activeStatus.value === 'Upcoming') {
            matchesStatus = course.start_date && course.start_date > today
        } else if (activeStatus.value === 'Live') {
            matchesStatus = course.start_date && course.start_date <= today && (!course.end_date || course.end_date >= today)
        } else if (activeStatus.value === 'Completed') {
            matchesStatus = course.end_date && course.end_date < today
        }
        
        // 3. Mode Logic
        const matchesMode = activeMode.value === 'All' || course.teaching_mode === activeMode.value
        
        return matchesSearch && matchesStatus && matchesMode
    })
})
</script>
