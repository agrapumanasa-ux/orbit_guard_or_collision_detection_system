def swarm_alert(objects, threshold=50):
    alerts = []

    for i in range(len(objects)):
        for j in range(i+1, len(objects)):
            dist = ((objects[i].position - objects[j].position)**2).sum()**0.5
            if dist < threshold:
                alerts.append((objects[i].id, objects[j].id, dist))

    return alerts
