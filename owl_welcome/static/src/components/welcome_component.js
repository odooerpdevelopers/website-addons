import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class WelcomeComponent extends Component {

    static template = "owl_welcome.WelcomeComponent";

    setup() {
        this.nextId = 1;
        this.state = useState({
            skills: [
                { id: this.nextId++, text: "🦉 Componente OWL creado ✅", completed: true },
                { id: this.nextId++, text: "📋 Template QWeb funcionando ✅", completed: true },
                { id: this.nextId++, text: "⚡ Estado reactivo con useState ✅", completed: true },
                { id: this.nextId++, text: "🔧 Registry pattern aplicado ✅", completed: true },
                { id: this.nextId++, text: "🚀 Client Action Launcher ✅", completed: true }
            ]
        });
    }

    removeSkill(skillId) {
        console.log(skillId)
        this.state.skills = this.state.skills.filter(skill => skill.id !== skillId);
    }

}



// Registro usando patrón real del proyecto
registry.category("actions").add("owl_welcome_component", WelcomeComponent);
