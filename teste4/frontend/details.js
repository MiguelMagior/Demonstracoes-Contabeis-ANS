const { createApp } = Vue

createApp({
  data() {
    return {
      cnpj: null,
      company: {},
      expenses: [],
      loading: false
    }
  },

  methods: {
    getCnpjFromUrl() {
      const params = new URLSearchParams(window.location.search)
      return params.get('cnpj')
    },

    async fetchCompanyDetails() {
      this.loading = true

      try {
        const compResponse = await axios.get(
          `http://localhost:8000/api/operadoras/${this.cnpj}`
        )
        this.company = compResponse.data

        const expResponse = await axios.get(
          `http://localhost:8000/api/operadoras/${this.cnpj}/despesas`
        )
        this.expenses = expResponse.data

      } catch (err) {
        console.error('Error loading operator details')
      } finally {
        this.loading = false
      }
    },

    formatCurrency(value) {
      return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
      }).format(value)
    }
  },

  mounted() {
    this.cnpj = this.getCnpjFromUrl()
    if (this.cnpj) {
      this.fetchCompanyDetails()
    }
  }
}).mount('#app')
