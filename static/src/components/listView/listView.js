/* @odoo-module */

import { Component, useState, onWillUnmount } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks"


export class ListViewAction extends Component{
    static template = "real_estate.ListView";

    setup(){
        this.state = useState({
            'records' : []
        });
        this.orm = useService("orm");
        // this.rpc = useService("rpc");
        this.loadRecords();

        
        this.IntervalId =  setInterval(() => {this.loadRecords()},3000)
        onWillUnmount(() => {clearInterval(this.IntervalId)});
    };

    async loadRecords(){
            const result = await this.orm.searchRead("property",[],[]) 
            this.state.records = result;
        };
        
    async createRecord() {
        const newRecord = {
            name: "Proprty_from_orm_owl",
            postcode: "5564",
            date_availability: new Date().toISOString().split('T')[0],
        };
        try {
            const result = await this.orm.create("property", [newRecord]);
            if (result) {
                await this.loadRecords(); 
            }
        } catch (error) {
            console.error("Error creating record:", error);
        }
    }

    async deleteRecord(recordId) {
        try {
            const result = await this.orm.unlink("property", [recordId]); 
            if (result) {
                await this.loadRecords(); 
            }
        } catch (error) {
            console.error("Error deleting record:", error);
        }
    }



    // async loadRecords(){
    //         const result = await this.rpc("/web/dataset/call_kw",{
    //             model : "property",
    //             method : "search_read",
    //             args : [[]],
    //             kwargs : {fields : ['id','name','postcode','date_availability']},
    //         });
    //         this.state.records = result;
    //     };

}

registry.category("actions").add("real_estate.action_list_view",ListViewAction);