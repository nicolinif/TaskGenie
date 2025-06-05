<template>
  <div class="container mt-5">
    <h2 class="mb-4">🧠 TaskGenie – Asistente Inteligente de Tareas</h2>

    <textarea v-model="texto" class="form-control mb-3" rows="5"
      placeholder="Ej: Tengo que estudiar para el parcial de NT2 el viernes y llamar al médico mañana."></textarea>

    <button @click="enviarTexto" class="btn btn-primary mb-4">Generar tareas</button>

    <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>

    <div class="mt-5">
      <ul class="nav nav-tabs">
        <li class="nav-item">
          <button class="nav-link" :class="{ active: vista === 'pendientes' }" @click="vista = 'pendientes'">
            Pendientes
          </button>
        </li>
        <li class="nav-item">
          <button class="nav-link" :class="{ active: vista === 'completadas' }" @click="vista = 'completadas'">
            Completadas
          </button>
        </li>
      </ul>

      <ul class="list-group mt-3">
        <li v-for="tarea in tareasFiltradas" :key="tarea.id"
            class="list-group-item d-flex justify-content-between align-items-center"
            :class="{ 'list-group-item-success': tarea.completado }">
          <div>
            <h5>{{ tarea.titulo }}</h5>
            <p class="mb-1">{{ tarea.descripcion }}</p>
            <small class="text-muted">📅 {{ tarea.fecha }}</small>
          </div>
          <div>
            <button
              v-if="!tarea.completado"
              class="btn btn-sm btn-success me-2"
              @click="marcarCompletada(tarea.id)">
              ✅
            </button>
            <button class="btn btn-sm btn-danger" @click="eliminarTarea(tarea.id)">
              🗑
            </button>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const texto = ref('')
const tareas = ref([])
const error = ref('')
const vista = ref('pendientes')

const obtenerTareas = async () => {
  try {
    const res = await axios.get('http://localhost:5000/tareas')
    tareas.value = res.data
  } catch (err) {
    console.error('Error al obtener tareas:', err)
    error.value = 'Error al obtener tareas.'
  }
}

const enviarTexto = async () => {
  try {
    await axios.post('http://localhost:5000/procesar-texto', {
      texto: texto.value
    })
    texto.value = ''
    await obtenerTareas()
  } catch (err) {
    console.error('Error al procesar texto:', err)
    error.value = 'Error al procesar el texto.'
  }
}

const marcarCompletada = async (id) => {
  try {
    await axios.patch(`http://localhost:5000/tareas/${id}`)
    await obtenerTareas()
  } catch (err) {
    console.error('Error al marcar tarea como completada:', err)
  }
}

const eliminarTarea = async (id) => {
  try {
    await axios.delete(`http://localhost:5000/tareas/${id}`)
    await obtenerTareas()
  } catch (err) {
    console.error('Error al eliminar tarea:', err)
  }
}

const tareasFiltradas = computed(() =>
  tareas.value.filter(t => t.completado === (vista.value === 'completadas'))
)

onMounted(obtenerTareas)
</script>
