var req = new XMLHttpRequest();
var clients = []

$(document).ready(function() {

    function FeatureRequestModel() {
        var self = this;
        self.title = ko.observable();
        self.description = ko.observable();
        self.area = ko.observableArray();
        self.client = ko.observableArray();
        self.priority = ko.observableArray();
        self.targetDate = ko.observable("2018-06-30");
        self.selectedClient = ko.observable();
        self.selectedArea = ko.observable();
        self.selectedPriority = ko.observable();
        self.results = ko.observable();

        self.getUpdatedPriority = function(){
            getPriorityList(self.selectedClient());
        }

        function getPriorityList(client_id){
            $.getJSON('http://featurerequestwcf-env.2hgppihysk.us-west-2.elasticbeanstalk.com/api/v1/FeatureRequest/Client/' + client_id, function(data) {
                self.priority.removeAll()
                if (data.length == 0){
                    self.priority.push(1)
                } else {
                    data.forEach(function(item){
                        self.priority.push(item['priority'])
                    })
                }
            })
        }

        $.getJSON("http://featurerequestwcf-env.2hgppihysk.us-west-2.elasticbeanstalk.com/api/v1/Client", function(data) {
            data.forEach(function(item){
                self.client.push(item)
            })
            getPriorityList(self.client()[0]['id']);
        });

        $.getJSON("http://featurerequestwcf-env.2hgppihysk.us-west-2.elasticbeanstalk.com/api/v1/Area", function(data) {
            data.forEach(function(item){
                self.area.push(item)
            })
        });


        self.submitFeatureRequest = function() {
            var featureRequest = {}
            featureRequest['title'] = self.title()
            featureRequest['description'] = self.description()
            featureRequest['clientId'] = self.selectedClient()
            featureRequest['priority'] = self.selectedPriority()
            featureRequest['target'] = self.targetDate()
            featureRequest['areaId'] = self.selectedArea()

            req.open("POST", "http://featurerequestwcf-env.2hgppihysk.us-west-2.elasticbeanstalk.com/api/v1/FeatureRequest", false);
            req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
            req.send(JSON.stringify(featureRequest));
            if (req.status == 201)
                self.results("Feature Request successfully submitted. Thank you!");
                clearFeatureRequest();
        }

        function clearFeatureRequest(){
            self.title("");
            self.description("");
            self.targetDate = ko.observable("2018-06-30");
            self.selectedClient(self.client()[0]);
            self.selectedArea(self.area()[0]);
            self.selectedPriority(self.priority()[0]);
        }

    }

    ko.applyBindings(new FeatureRequestModel());

})