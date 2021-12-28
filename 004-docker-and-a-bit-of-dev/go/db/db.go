package cache

import (
	"time"
)

type Cache interface {
	Get(k string) (rv interface{}, err error)
	Put(k string, timeout time.Duration) (err error)
	Evict(k string) (err error)
}

type RedisCache struct {
	client interface{}
}

func NewRedisCache() *RedisCache {
	return &RedisCache{}
}

func (this *RedisCache) Get(k string) (rv interface{}, err error) {
	return
}

func (this *RedisCache) Put(k string, timeout time.Duration) (err error) {
	return
}

func (this *RedisCache) Evict(k string) (err error) {
	return
}
