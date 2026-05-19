<script setup>
import { ref } from 'vue';
import TheForm from './components/predictor-form/TheForm.vue';
import Dashboard from './components/dashboard/Dashboard.vue';
import './assets/base.css';
import './assets/main.css'

const activeTab = ref('predictor');
</script>

<template>
  <header>
    <h1>{{ activeTab === 'dashboard' ? 'Child Stunting Dashboard' : 'Child Stunting Predictor' }}</h1>
    <p>
      {{ activeTab === 'dashboard' ? 
      'This dashboard presents the EDA methods performed on the child stunting dataset, exploring the various trends in the child stunting data.' : 
      'This predictor uses the LightGBM model, and has been trained on datasets containing records of children from Balochistan, Sindh and KPK.' 
       }}
    </p>

    <!-- <div class="wrapper">
      <HelloWorld msg="You did it!" />
    </div> -->
  </header>

  <main>

    <div class="toggle-bar">
      <button 
        :class="{ active: activeTab === 'dashboard' }"
        @click="activeTab = 'dashboard'"
      >
        Dashboard
      </button>
      <button 
        :class="{ active: activeTab === 'predictor' }"
        @click="activeTab = 'predictor'"
      >
        Predictor
      </button>
    </div>

    <TheForm v-if="activeTab === 'predictor'" />
    <Dashboard v-if="activeTab === 'dashboard'" />
    
  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    margin: 20px auto;
    width: 40rem;

    display: flex;
    flex-direction: column;

    place-items: center;
    
  }

  header h1 {
    padding-bottom: 8px;
    font-weight: bold;
    color: var(--color-heading);
  }
  
  header p {
    text-align: center;
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  main {
    color: var(--color-text);
  }
}
</style>
