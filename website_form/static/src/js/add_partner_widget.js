/** @odoo-module  **/

import publicWidget from '@web/legacy/js/public/public_widget';
console.log("add partner widget is loaded...")

publicWidget.registry.AddPartnerWidget = publicWidget.Widget.extend({
    'selector': '#main_addpartner',

    'events': {
        'click #exampleCheck1': '_oneClickCheckBox',
    },

    init(parent, options){
        this._super(...arguments);
        console.log("override init add partner widget success")

    },

    _oneClickCheckBox() {
        console.log("click checkbox...")

    }

});


export default publicWidget.registry.AddPartnerWidget;
