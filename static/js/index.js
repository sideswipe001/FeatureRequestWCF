var req = new XMLHttpRequest();
var clients = []

var url = window.location.href;

$(document).ready(function() {
    $( "#datepicker" ).datepicker();

    function FeatureRequestModel() {
        var self = this;
        var areaMap = {};
        var clientMap = {};
        self.title = ko.observable();
        self.description = ko.observable();
        self.area = ko.observableArray();
        self.client = ko.observableArray();
        self.priority = ko.observableArray();
        self.targetDate = ko.observable();
        self.selectedClient = ko.observable();
        self.selectedClientName = ko.observable();
        self.selectedArea = ko.observable();
        self.selectedPriority = ko.observable();
        self.submitMessage = ko.observable();
        self.clientRequests = ko.observableArray();

        self.getUpdatedData = function(){
            getPriorityList(self.selectedClient());
            updateFeatureRequestsList(self.selectedClient());
        }

        self.selectedClient.subscribe(function(){
            self.selectedClientName(clientMap[self.selectedClient()])
        });

        self.client.subscribe(function(){
            self.selectedClientName(clientMap[self.selectedClient()])
        });

        function getPriorityList(client_id){
            $.getJSON(url + '/api/v1/FeatureRequest/Client/' + client_id, function(data) {
                var lowestPriority = 1;
                self.priority.removeAll()
                if (data.length == 0){
                    self.priority.push(1)
                } else {
                    data.forEach(function(item){
                        var itemPriority = item['priority']
                        self.priority.push(itemPriority)
                        if (itemPriority > lowestPriority)
                            lowestPriority = itemPriority;
                    })
                    self.priority.push(lowestPriority+1);
                }
                self.priority.sort(function(left, right){ return parseInt(left) == parseInt(right) ? 0 : (parseInt(left) < parseInt(right) ? -1 : 1) });
            })
        }

        function updateFeatureRequestsList(client_id){
            self.clientRequests.removeAll()
            $.getJSON(url + '/api/v1/FeatureRequest/Client/' + client_id, function(data) {
                data.forEach(function(item){
                    item.areaId = areaMap[item.areaId]
                    if (item.target)
                        item.target = new Date(item.target).toISOString().split('T')[0]

                    self.clientRequests.push(item)
                })
                sortClientRequests();
            });
        }


        $.getJSON(url + "/api/v1/Client", function(data) {
            data.forEach(function(item){
                self.client.push(item)
                clientMap[item.id] = item.name;
            })
            getPriorityList(self.client()[0]['id']);
        });

        $.getJSON(url + "/api/v1/Area", function(data) {
            data.forEach(function(item){
                self.area.push(item)
                areaMap[item.id] = item.name;
            })
        });

        function submitFeatureRequest() {
            var featureRequest = {}
            featureRequest['title'] = self.title()
            featureRequest['description'] = self.description()
            featureRequest['clientId'] = self.selectedClient()
            featureRequest['priority'] = self.selectedPriority()
            featureRequest['target'] = new Date(self.targetDate()).toISOString().split('T')[0]
            featureRequest['areaId'] = self.selectedArea()

            $.getJSON(url + '/api/v1/FeatureRequest/Client/' + self.selectedClient(), function(data) {
                data.forEach(function(item){
                    if (item['priority'] >= self.selectedPriority()){
                        var newPriority = item['priority']+1;
                        item['priority'] = newPriority;
                        item['target'] = new Date(item.target).toISOString().split('T')[0]
                        $.ajax({
                            type: "POST",
                            url: url + "/api/v1/FeatureRequest/"+ item.id,
                            async: true,
                            data: JSON.stringify(item),
                            contentType: 'application/json',
                        })
                    }
                })
                $.ajax({
                type: "POST",
                url: url + "/api/v1/FeatureRequest",
                async: true,
                data: JSON.stringify(featureRequest),
                success: function(){
                    self.submitMessage("Feature Request successfully submitted. Thank you!");
                    featureRequest.areaId = areaMap[featureRequest.areaId];
                    updateFeatureRequestsList(self.selectedClient());
                    getPriorityList(self.selectedClient());
                    clearFeatureRequest();
                },
                contentType: 'application/json'
                })
            });
        }

        self.validateInput = function(){
            if ($.trim(self.title()) == ""){
                self.submitMessage("Please include a title before sumbitting.")
                return;
            }
            if ($.trim(self.description()) == ""){
                self.submitMessage("Please include a description before sumbitting.")
                return;
            }
            if (isNaN(Date.parse(self.targetDate()))){
                self.submitMessage("Please make sure Target Date is a valid date format.")
                return;
            }
            submitFeatureRequest();
        };

        function sortClientRequests(){
            self.clientRequests.sort(function(left, right) { return left.priority == right.priority ? 0 : (left.priority < right.priority ? -1 : 1) })
        }

        function clearFeatureRequest(){
            self.title("");
            self.description("");
            self.targetDate("");
        }

    }

    ko.applyBindings(new FeatureRequestModel());

})