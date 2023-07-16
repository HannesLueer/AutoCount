package mqtt

import (
	"encoding/json"
	"github.com/mochi-co/mqtt/v2"
	"github.com/mochi-co/mqtt/v2/hooks/auth"
	"github.com/mochi-co/mqtt/v2/listeners"
	"log"
	"server/src/models"
)

var mqttServer *mqtt.Server

func InitMqtt() {
	// Create the new MQTT Server.
	mqttServer = mqtt.New(nil)

	// Allow all connections but no clients have publishing permissions
	err := mqttServer.AddHook(new(auth.Hook), &auth.Options{
		Ledger: &auth.Ledger{
			Auth: auth.AuthRules{
				{Allow: true},
			},
			ACL: auth.ACLRules{
				{
					Filters: auth.Filters{
						"#": auth.ReadOnly,
					},
				},
			},
		},
	})
	if err != nil {
		log.Fatal(err)
	}

	// Create a TCP listener on a standard port.
	tcp := listeners.NewTCP("t1", ":1883", nil)
	err = mqttServer.AddListener(tcp)
	if err != nil {
		log.Fatal(err)
	}

	err = mqttServer.Serve()
	if err != nil {
		log.Fatal(err)
	}
}

func Publish(siteId string, counter models.CounterOut) (err error) {
	jsonResp, err := json.Marshal(counter)
	if err != nil {
		return err
	}

	err = mqttServer.Publish(siteId, jsonResp, false, 0)
	return err
}
