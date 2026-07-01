<template>
  <v-container>
    <h1>Artists</h1>

    
    <v-text-field v-model="newArtist" label="Ime" />
    <v-text-field v-model="newAlbum" label="Album" />
    <v-text-field v-model="newYear" label="Godina" />

    <v-btn color="primary" class="mb-4" @click="addArtist">
      Dodaj
    </v-btn>

    <v-divider class="my-4" />

    
    <v-table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Ime</th>
          <th>Album</th>
          <th>Godina</th>
          <th>Akcije</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="artist in artists" :key="artist.id">
          <td>{{ artist.id }}</td>

          <td>
            <span v-if="editIndex !== artist.id">
              {{ artist.name }}
            </span>
            <v-text-field v-else v-model="editName" />
          </td>

          <td>{{ artist.album }}</td>
          <td>{{ artist.year }}</td>

          <td>
            <v-btn
              v-if="editIndex !== artist.id"
              size="small"
              color="blue"
              @click="startEdit(artist)"
            >
              Edit
            </v-btn>

            <v-btn
              v-else
              size="small"
              color="green"
              @click="saveEdit(artist.id)"
            >
              Save
            </v-btn>

            <v-btn
              size="small"
              color="red"
              @click="deleteArtist(artist.id)"
            >
              Delete
            </v-btn>
          </td>
        </tr>
      </tbody>
    </v-table>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const API = 'http://127.0.0.1:5000/artists'

const artists = ref([])

const newArtist = ref('')
const newAlbum = ref('')
const newYear = ref('')

const editIndex = ref(null)
const editName = ref('')


const fetchArtists = async () => {
  const res = await axios.get(API)
  artists.value = res.data
}


const addArtist = async () => {
  await axios.post(API, {
    name: newArtist.value,
    album: newAlbum.value,
    year: newYear.value
  })

  newArtist.value = ''
  newAlbum.value = ''
  newYear.value = ''

  fetchArtists()
}


const deleteArtist = async (id) => {
  await axios.delete(`${API}/${id}`)
  fetchArtists()
}


const startEdit = (artist) => {
  editIndex.value = artist.id
  editName.value = artist.name
}


const saveEdit = async (id) => {
  await axios.put(`${API}/${id}`, {
    name: editName.value
  })

  editIndex.value = null
  editName.value = ''

  fetchArtists()
}

onMounted(fetchArtists)
</script>