# icinga2-notification-yeelight

A script that will change the Yeelight color depending on the current host/service state.

For example, when a service/host reaches a critical state, this script will then change the color of the Yeelight to red and blink 3 times. See the table below to see which color will be set on a specfic state.

| State    | Color  |
|----------|--------|
| CRITICAL | Red    |
| DOWN 	   | Red    |
| WARNING  | Yellow |
| OK       | Green  |
| UP       | Green  |

Example icinga2 `NotificationCommand` configuration:

```
object NotificationCommand "yeelight-service-notification" {
	command = [ PathToScript ]
	env += {
		STATE = "$service.state$"
	}
}

```

If you think this code can be improved, dont hesitate to open a PR! :-)
