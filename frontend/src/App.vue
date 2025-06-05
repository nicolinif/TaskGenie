<template>
  <div class="container mt-5">
    <h2 class="mb-4">🧠 TaskGenie – Asistente Inteligente de Tareas</h2>

    <textarea v-model="texto" class="form-control mb-3" rows="5" placeholder="Ej: Tengo que estudiar para el parcial de NT2 el viernes y llamar al médico mañana."></textarea>

    <button @click="enviarTexto" class="btn btn-primary mb-4">Generar tareas</button>

    <div v-if="tareas.length > 0">
      <h4>📝 Tareas generadas:</h4>
      <div v-for="(tarea, index) in tareas" :key="index" class="card my-2 p-3">
        <p><strong>Tarea:</strong> {{ tarea.tarea }}</p>
        <p><strong>Fecha:</strong> {{ tarea.fecha }}</p>
        <p><strong>Prioridad:</strong> {{ tarea.prioridad }}</p>
      </div>
    </div>

    <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      texto: '',
      tareas: [],
      error: ''
    }
  },
  methods: {
    async enviarTexto() {
  this.error = ''
  this.tareas = []
  try {
    const response = await axios.post('http://localhost:5000/procesar-texto', {
      texto: this.texto
    })

    console.log("RESPUESTA BRUTA:", response.data.tareas) // 👈 Asegurate de que esté después

    const parsed = JSON.parse(response.data.tareas)
    this.tareas = parsed
  } catch (err) {
    this.error = 'Error al procesar el texto. Verificá que el backend esté corriendo.'
    console.error(err)
  }
}

  }
}
</script>
