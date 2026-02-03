const {createApp} = Vue

createApp({
    data() {
        return {
            // tabela
            companies: [],
            search: '',
            page: 1,
            limit: 10,
            loading: false,
            error: null,

            // gráfico
            chart: null
        }
    },

    methods: {
        async fetchCompanies() {
            this.loading = true
            this.error = null

            try {
                const response = await axios.get(
                    'http://localhost:8000/api/operadoras',
                    {
                        params: {
                            page: this.page,
                            limit: this.limit,
                            search: this.search
                        }
                    }
                )

                this.companies = response.data.data

            } catch (err) {
                this.error = 'Erro carregando operadoras'
                console.error(err)
            } finally {
                this.loading = false
            }
        },

        async fetchStatistics() {
            try {
                const response = await axios.get(
                    'http://localhost:8000/api/estatisticas'
                )

                const expensesByUf = response.data.despesas_por_uf
                expensesByUf.sort((a, b) => b.total - a.total)

                const labels = expensesByUf.map(item => item.uf)
                const values = expensesByUf.map(item => item.total)

                this.renderChart(labels, values)

            } catch (err) {
                console.error('Erro ao carregar estatisticas', err)
            }
        },

        formatCurrency(value) {
            return new Intl.NumberFormat('pt-BR', {
                style: 'currency',
                currency: 'BRL'
            }).format(value)
        },

        renderChart(labels, values) {
            const canvas = document.getElementById('expensesChart')
            if (!canvas) return

            const ctx = canvas.getContext('2d')

            if (this.chart) {
                this.chart.destroy()
            }

            this.chart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Despesas totais por UF (R$)',
                            data: values
                        }
                    ]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            ticks: {
                                callback: (value) => {
                                    return new Intl.NumberFormat('pt-BR', {
                                        style: 'currency',
                                        currency: 'BRL'
                                    }).format(value)
                                }
                            }
                        }
                    }
                }
            })
        },

        nextPage() {
            this.page++
            this.fetchCompanies()
        },

        prevPage() {
            if (this.page > 1) {
                this.page--
                this.fetchCompanies()
            }
        }
    },

    watch: {
        search() {
            this.page = 1
            this.fetchCompanies()
        }
    },

    mounted() {
        this.fetchCompanies()
        this.fetchStatistics()
    }
}).mount('#app')
