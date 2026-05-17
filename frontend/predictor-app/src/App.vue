<script setup>
import TheForm from './components/predictor-form/TheForm.vue';
import './assets/base.css';
</script>

<template>
  <header>
    <h1>Child Stunting Predictor</h1>
    <p>
      This predictor uses the LightGBM model, and has been trained on datasets containting
      records of children from Balochistan, Sindh and KPK.
    </p>

    <!-- <div class="wrapper">
      <HelloWorld msg="You did it!" />
    </div> -->
  </header>

  <main>
    <TheForm />
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
    /* border: solid blanchedalmond 1px; */
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
    margin: 0 16rem;
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
