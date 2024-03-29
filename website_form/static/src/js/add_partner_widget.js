/** @odoo-module  **/

import publicWidget from '@web/legacy/js/public/public_widget';

console.log("add partner widget is loaded...")

publicWidget.registry.AddPartnerWidget = publicWidget.Widget.extend({
    'selector': '#main_addpartner',

    'events': {
        'click #exampleCheck1': '_oneClickCheckBox',
    },

    init(parent, options) {
        this._super(...arguments);
        //this.orm = this.bindService("orm")
        console.log("override init add partner widget success")

    },

    async start() {
        const res = await this._super(...arguments);
        this.checkbox = this.el.querySelector('#exampleCheck1');
        return res
    },

    _oneClickCheckBox() {
        console.log("click checkbox...")
        if(this.checkbox.checked){
            this.$el.find('#show_countries').removeClass('d-none')
        }else{
            this.$el.find('#show_countries').addClass('d-none')
        }
    },

});


export default publicWidget.registry.AddPartnerWidget;
