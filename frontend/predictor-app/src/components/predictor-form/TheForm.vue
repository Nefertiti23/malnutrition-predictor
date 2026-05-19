<script setup>
import { ref } from 'vue'
import './Form.css'

// 1. Create reactive data trackers for your form fields
const childAge = ref('')
const motherEducation = ref('')
const wealthIndex = ref('')
const urbanRural = ref(0)
const province = ref(0)

// Trackers for handling the backend response state
const predictionResult = ref(null)
const isLoading = ref(false)
const errorMessage = ref('')

// 2. The function that sends data to your running Flask server
async function handlePrediction() {
  isLoading.value = true
  errorMessage.value = ''
  predictionResult.value = null

  const payload = {
    child_age_months: parseFloat(childAge.value),
    mother_education: parseFloat(motherEducation.value),
    wealth_index: parseFloat(wealthIndex.value),
    urban_rural: parseFloat(urbanRural.value),
    province: parseFloat(province.value)
  }

  try {
    const apiUrl = import.meta.env.VITE_API_URL
    let endpoint
    
    if (apiUrl && apiUrl !== '/api') {
      // Railway: use /predict endpoint
      endpoint = `${apiUrl}/predict`
    } else {
      // Vercel: use /api endpoint
      endpoint = '/api'
    }
    
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    })

    if (!response.ok) {
      throw new Error('Backend server returned an error error.')
    }

    const data = await response.json()
    
    // Save the output (0 or 1) returned from LightGBM
    predictionResult.value = data.prediction
  } catch (error) {
    errorMessage.value = 'Could not connect to the backend API. Please try again.'
    console.error(error)
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <form @submit.prevent="handlePrediction">
    <div class="input-box">
        <label>Child Age (in months)</label>
        <input type="number" v-model="childAge" required min="0">
    </div>
    <div class="divider-line"></div>
    
    <div class="input-box">
        <label>Mother's Education</label>
        <p>On a scale of 1 - 5</p>
        <input type="number" v-model="motherEducation" required min="1" max="5">
    </div>
    <div class="divider-line"></div>
    
    <div class="input-box">
        <label>Wealth Index</label>
        <p>On a scale of 1 - 5</p>
        <input type="number" v-model="wealthIndex" required min="1" max="5">
    </div>
    <div class="divider-line"></div>
    
    <div class="input-box">
        <label>District Type</label>
        <p>Urban or rural?</p>
        <select id="district_type" name="district_type" v-model="urbanRural">
            <option :value="0">Rural</option>
            <option :value="1">Urban</option>
        </select>
    </div>
    <div class="divider-line"></div>
    
    <div class="input-box">
        <label>Province</label>
        <select id="province" name="province" v-model="province">
            <option :value="0">Sindh</option>
            <option :value="1">Balochistan</option>
            <option :value="2">KPK</option>
        </select>
    </div>
    <div class="divider-line"></div>

    <div class="button-box" style="margin-top: 20px; text-align: center;">
      <button type="submit" :disabled="isLoading" style="padding: 10px 20px; cursor: pointer; font-weight: bold;">
        {{ isLoading ? 'Calculating...' : 'Make Prediction' }}
      </button>
    </div>

    <div v-if="predictionResult !== null" class="result-box" style="margin-top: 25px; padding: 15px; border: 2px solid green; text-align: center; border-radius: 8px; background-color: #f0fff0;">
      <h3 style="color: green; margin: 0;">Prediction Output: <span style="font-weight: bold;"> {{Boolean(predictionResult)}}</span></h3>
      <p style="margin: 5px 0 0 0; color: #333;">
        {{ predictionResult === 1 ? 'High Risk of Child Stunting detected.' : 'Low/Normal Risk of Child Stunting detected.' }}
      </p>
    </div>

    <div v-if="errorMessage" class="error-box" style="margin-top: 25px; padding: 15px; border: 2px solid red; text-align: center; border-radius: 8px; background-color: #fff5f5; color: red;">
      {{ errorMessage }}
    </div>
  </form>
</template>