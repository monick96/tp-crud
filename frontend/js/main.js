if (document.getElementById("app")) {
    const { createApp } = Vue
 
    createApp({data() {
        return {
            ofertas: [],
            errored: false,
            loading: true,
            url: "http://localhost:5000/ofertas"
            }
    },
    methods: {
        fetchData(url) {
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    this.ofertas = data;
                    this.loading = false;
                })
                .catch(err => {
                    this.errored = true
                })
        },
        eliminar(oferta) {
            const url = 'http://localhost:5000/ofertas/' + oferta;
            var options = {
                method: 'DELETE',
            }
            fetch(url, options)
                .then(res => res.text()) // or res.json()
                .then(res => {
                    location.reload();
                })
        }
    },
    created() {
        this.fetchData(this.url)
    }
}).mount('#app')
}
